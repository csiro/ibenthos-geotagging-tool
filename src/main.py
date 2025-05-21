import datetime
import hashlib
import logging
import os
import shutil
import sys
import threading
import zoneinfo
from pathlib import Path
from typing import Optional

import gpxpy
import numpy as np
from exiftool import ExifToolHelper
from geotag_pt import PhotoTransectGPSTagger
from PIL import Image
from PyQt6.QtCore import QObject, QThread, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

import models
from ifdo import IFDOModel

logger = logging.getLogger(__name__)



def _get_images(directory: Path):
    extensions = ['.jpg', '.jpeg', '.png']
    if not directory.exists() or not directory.is_dir():
        return []
    file_list = list(directory.rglob("*"))
    return [file for file in file_list if file.suffix.lower() in extensions]



def get_shannon_entropy(image_data: Image.Image) -> float:
    """
    Calculate the Shannon entropy of an image file.

    Args:
        image_data: The loaded image data.

    Returns:
        The Shannon entropy of the image as a float value.
    """
    # Convert to grayscale
    grayscale_image = image_data.convert("L")

    # Calculate the histogram
    histogram = np.array(grayscale_image.histogram(), dtype=np.float32)

    # Normalize the histogram to get probabilities
    probabilities = histogram / histogram.sum()

    # Filter out zero probabilities
    probabilities = probabilities[probabilities > 0]

    # Calculate Shannon entropy
    entropy = -np.sum(probabilities * np.log2(probabilities))

    return float(entropy)


def get_average_image_color(image_data: Image.Image) -> tuple[int, ...]:
    """
    Calculate the average color of an image.

    Args:
        image_data: The loaded image data.

    Returns:
        A list of integers representing the average color of the image in RGB format. Each element in the list
        corresponds to the average intensity of the Red, Green, and Blue channels, respectively.

        Note: If the input image is None, None will be returned.
    """
    # Convert the image to numpy array
    np_image = np.array(image_data)

    # Calculate the average color for each channel
    average_color = np.mean(np_image, axis=(0, 1))

    return tuple(map(int, average_color))


class GeotagWorker(QObject):
    progress = pyqtSignal(int, int)
    error_msgs = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, tagger: PhotoTransectGPSTagger, import_dir: Path, export_dir: Path,
                       ifdo_model: Optional[IFDOModel] = None, exec_path: Optional[str] = None):
        super().__init__()
        self.tagger = tagger
        self.import_dir = import_dir
        self.export_dir = export_dir

        self.ifdo_model = ifdo_model
        self.exec_path = exec_path

    def add_to_ifdo(self, relative_fn: str, exif_data: dict, gps_tags: dict):
        image_datetime = datetime.datetime.strptime(f'{gps_tags["Exif:GPSDateStamp"]} {gps_tags["Exif:GPSTimeStamp"]}',
                                                    '%Y:%m:%d %H:%M:%S').replace(tzinfo=datetime.UTC)
        image_latitude = float(gps_tags["Composite:GPSPosition"].split(" ")[0])
        image_longitude = float(gps_tags["Composite:GPSPosition"].split(" ")[1])

        hasher = hashlib.sha256()

        with open(self.export_dir / relative_fn, 'rb') as f:
            while chunk := f.read(1_048_576):  # 1MB chunks
                hasher.update(chunk)

        image_hash_sha256 = hasher.hexdigest()

        if 'EXIF:Make' in exif_data and 'EXIF:Model' in exif_data:
            image_platform = f"{exif_data['EXIF:Make']} {exif_data['EXIF:Model']}"
        else:
            image_platform = "Unknown"

        with Image.open(self.export_dir / relative_fn) as img:
            image_entropy = get_shannon_entropy(img)
            image_average_color = get_average_image_color(img)

        self.ifdo_model.add_image_properties(
            image_relative_path=str(relative_fn),
            image_datetime=image_datetime,
            image_latitude=image_latitude,
            image_longitude=image_longitude,
            image_platform=image_platform,
            image_sensor="Unknown",
            image_hash_sha256=image_hash_sha256,
            image_entropy=image_entropy,
            image_average_color=[*image_average_color]
        )

    def run(self):
        # Get images to be tagged
        image_list = _get_images(self.import_dir)

        total_images = len(image_list)

        tally = 0
        with ExifToolHelper(executable=self.exec_path) as et:
            for image_fn in image_list:
                relative_fn = image_fn.relative_to(self.import_dir)
                exif_data = et.get_metadata(str(image_fn))[0]
                try:
                    gps_tags = self.tagger.generate_gps_tags(exif_data)
                except IndexError as e:
                    logger.error(
                        "Image %s not within range of GPX file. Skipping this image.", image_fn
                    )
                    self.error_msgs.emit(
                        f"Image {image_fn} not within range of GPX file. Skipping this image."
                    )
                    logger.error(e)
                    continue
                except AssertionError as _:
                    logger.error(
                        "Image %s does not contain time data. Skipping this image.", image_fn
                    )
                    self.error_msgs.emit(
                        f"Image {image_fn} does not contain time data. Skipping this image."
                    )
                    continue
                save_fn = self.export_dir / relative_fn
                save_fn.parent.mkdir(parents=True, exist_ok=True)
                if not save_fn.parent.exists():
                    logger.error("Failed to create directory %s", save_fn.parent)
                    continue
                shutil.copy2(image_fn, save_fn)
                et.set_tags(files=save_fn, tags=gps_tags, params=['-overwrite_original'])
                if self.ifdo_model is not None:
                    self.add_to_ifdo(relative_fn, exif_data, gps_tags)
                logger.info("Image %s geotagged and saved to %s", image_fn, save_fn)
                tally += 1
                self.progress.emit(tally, total_images)
        # Save the IFDO model to a file
        if self.ifdo_model is not None:
            ifdo_path = self.export_dir / "ifdo.yml"
            self.ifdo_model.export_ifdo_yaml(str(ifdo_path))
            logger.info("IFDO file saved to %s", ifdo_path)
        self.finished.emit("Finished geotagging images.")

class MainController(QObject):
    def __init__(self, model: models.UserInputModel, config: models.ConfigModel,
                       feedback: models.FeedbackModel, exec_path: Optional[str] = None):
        super().__init__()
        self._model = model
        self._config = config
        self._model.importDirectoryChanged.connect(self.countImages)
        self._feedback = feedback
        self._worker = None
        self._workerthread = None
        self._exec_path = exec_path

    # Slot used to average the GPX file data to provide an estimated site location
    @pyqtSlot(str)
    def gpxFileSelected(self, path):
        threading.Thread(target=self._process_gpx_file, args=(path,)).start()

    def _process_gpx_file(self, path):
        # Open the GPX file and read the data
        with open(path.replace("file://", ""), "r", encoding="utf-8") as file:
            gpx = gpxpy.parse(file)

        avg_lat, avg_lon, _ = self._get_average_gpx(gpx)
        if self._model.siteLatitude == "":
            self._model.siteLatitude = f"{avg_lat:.08f}"
        if self._model.siteLongitude == "":
            self._model.siteLongitude = f"{avg_lon:.08f}"

    def _get_average_gpx(self, gpx_data):
        avg_lat = 0
        avg_lon = 0
        avg_ele = 0
        count = 0
        for track in gpx_data.tracks:
            for segment in track.segments:
                for point in segment.points:
                    avg_lat += point.latitude
                    avg_lon += point.longitude
                    avg_ele += point.elevation
                    count += 1
        avg_lat /= count
        avg_lon /= count
        avg_ele /= count
        return avg_lat, avg_lon, avg_ele

    # Slot used to assist in setting start and stop times based on the GPS photo date
    @pyqtSlot(str)
    def gpsPhotoDateSet(self, date):
        if self._model.collectionStartDate == "":
            self._model.collectionStartDate = date
        if self._model.collectionEndDate == "":
            self._model.collectionEndDate = date

    # Slot to calculate number of images in the import directory
    @pyqtSlot(str, result=int)
    def countImages(self, directory):
        path = Path(directory.replace("file://", ""))
        if not path.exists() or not path.is_dir():
            return 0
        image_list = _get_images(path)
        return len(image_list)

    # Slot to start the geotagging process
    @pyqtSlot(result=bool)
    def geotag(self):
        # Clear any previous feedback
        self._feedback.feedbackText = ""
        # Validate the input
        validator = models.UserInputModelValidator()
        self._feedback.feedbackText = "Validating input...\n"
        if not validator.validate(self._model):
            self._feedback.addFeedbackLine("Validation failed")
            for error in validator.latest_errors:
                self._feedback.addFeedbackLine(error)
            return False

        # Create the PhotoTransectGPSTagger object
        jpg_gps_timestamp = datetime.datetime.fromisoformat(
            self._model.gpsDate + " " + self._model.gpsTime
        )
        if self._config.useWorkaround:
            jpg_gps_timestamp = jpg_gps_timestamp.replace(tzinfo=models.TimezoneWorkaround(
                self._config.gpsTimezoneOptions[self._model.gpsTimezoneIndex])
            )
        else:
            jpg_gps_timestamp = jpg_gps_timestamp.replace(tzinfo=zoneinfo.ZoneInfo(
                self._config.gpsTimezoneOptions[self._model.gpsTimezoneIndex])
            )
        tagger = PhotoTransectGPSTagger.from_files(
            self._model.gpxFilepath.replace("file://", ""),
            self._model.gpsPhotoFilepath.replace("file://", ""),
            jpg_gps_timestamp,
            exiftool_path=self._exec_path
        )

        # Create the IFDO model
        if self._model.ifdoEnable:
            ifdo_model = IFDOModel(image_set_name=self._model.imageSetName,
                                   image_context=self._model.imageContext,
                                   image_project=self._model.projectName,
                                   image_event=self._model.campaignName,
                                   image_pi=(self._model.piName, self._model.piORCID if self._model.piORCID != "" else "0000-0000-0000-0000"),
                                   image_creators=[(self._model.collectorName, self._model.collectorORCID if self._model.collectorORCID != "" else "0000-0000-0000-0000")],
                                   image_copyright=self._model.organisation,
                                   image_license=self._model.license,
                                   image_abstract=self._model.imageAbstract,
                                   image_objective=self._model.imageObjective,
                                   image_meters_above_ground=float(self._model.distanceAboveGround))
        else:
            ifdo_model = None

        # Create new worker thread
        self._workerthread = QThread()
        import_dir = Path(self._model.importDirectory.replace("file://", ""))
        export_dir = Path(self._model.exportDirectory.replace("file://", ""))
        self._worker = GeotagWorker(tagger, import_dir, export_dir, ifdo_model=ifdo_model,
                                    exec_path=self._exec_path)
        self._worker.moveToThread(self._workerthread)
        self._workerthread.started.connect(self._worker.run)
        self._worker.progress.connect(self._feedback.updateProgress)
        self._worker.finished.connect(self._workerthread.quit)
        self._worker.error_msgs.connect(self._feedback.addFeedbackLine)
        self._worker.finished.connect(self._feedback.addFeedbackLine)
        self._worker.finished.connect(self._worker.deleteLater)
        self._workerthread.finished.connect(self._workerthread.deleteLater)
        self._workerthread.start()
        self._feedback.addFeedbackLine("Geotagging images...")
        return True

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    user_input_model = models.UserInputModel()
    config_model = models.ConfigModel()
    feedback_model = models.FeedbackModel()

    # Determine if we're a package or running as a script
    if getattr(sys, "frozen", False):
        logger.info("Running as a package")
        app_path = Path(sys._MEIPASS)
        exiftool_path = str(app_path / "bin" / "exiftool")
        build_id_path = app_path / "build_id.txt"
        if build_id_path.exists():
            with open(build_id_path, "r") as f:
                config_model.buildHash = f.read().strip()
            logger.info("Build ID: %s", config_model.buildHash)
        else:
            logger.warning("Build ID file not found.")
    else:
        app_path = Path(os.path.dirname(os.path.realpath(__file__)))
        exiftool_path = None

    controller = MainController(user_input_model, config_model, feedback_model,
                                exec_path=exiftool_path)

    engine.rootContext().setContextProperty("userInputModel", user_input_model)
    engine.rootContext().setContextProperty("configModel", config_model)
    engine.rootContext().setContextProperty("feedbackModel", feedback_model)
    engine.rootContext().setContextProperty("controller", controller)
    config_model.initialise()
    engine.load((app_path / "main.qml").as_uri())


    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

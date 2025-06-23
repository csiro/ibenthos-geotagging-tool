"""
main.py: Main entry point for the iBenthos Geotagging Tool application.
This script initializes the application, sets up the main controller, and starts the Qt event loop.

Copyright (c) 2023-2025
Commonwealth Scientific and Industrial Research Organisation (CSIRO)
ABN 41 687 119 230

Author: Brendan Do <brendan.do@csiro.au>
"""
import copy
import datetime
import hashlib
import logging
import os
import shutil
import sys
import zoneinfo
from pathlib import Path
from typing import Optional

import numpy as np
from exiftool import ExifToolHelper
from geotag_pt import PhotoTransectGPSTagger
from PIL import Image
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication

import models
import views
from ifdo import IFDOModel
from imagekmlgen import ImageKMLGenerator

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
        A list of integers representing the average color of the image in RGB format. Each element
        in the list corresponds to the average intensity of the Red, Green, and Blue channels,
        respectively.

        Note: If the input image is None, None will be returned.
    """
    # Convert the image to numpy array
    np_image = np.array(image_data)

    # Calculate the average color for each channel
    average_color = np.mean(np_image, axis=(0, 1))

    return tuple(map(int, average_color))

class GeotagWorker(QObject):
    """
    Worker class that contains the geotagging logic intended to be run as a separate thread.
    """
    progress = Signal(int, int)
    error_msgs = Signal(str)
    finished = Signal(str)

    def __init__(self, tagger: PhotoTransectGPSTagger, import_dir: Path, export_dir: Path,
                       ifdo_model: Optional[IFDOModel] = None, exec_path: Optional[str] = None,
                       tz_override: Optional[str] = None, kml_export: bool = False):
        super().__init__()
        self.tagger = tagger
        self.import_dir = import_dir
        self.export_dir = export_dir
        self.tz_override = tz_override

        self.ifdo_model = ifdo_model
        self.exec_path = exec_path
        self.kml_export = kml_export
        self.base_tags = {}

    def set_base_tags(self, base_tags: dict):
        """
        Set the base tags for the images. This is used to set common metadata for all images.
        """
        self.base_tags = base_tags

    def add_to_ifdo(self, relative_fn: str, exif_data: dict, gps_tags: dict):
        """
        Add image properties to the IFDO model.
        """
        image_datetime = datetime.datetime.strptime(f'{gps_tags["Exif:GPSDateStamp"]} ' + \
                                                    f'{gps_tags["Exif:GPSTimeStamp"]}',
                                                    '%Y:%m:%d %H:%M:%S')\
                                                    .replace(tzinfo=datetime.UTC)
        image_latitude = float(gps_tags["Composite:GPSPosition"].split(" ")[0])
        image_longitude = float(gps_tags["Composite:GPSPosition"].split(" ")[1])

        hasher = hashlib.sha256()

        with open(self.export_dir / relative_fn, 'rb') as image_file:
            while chunk := image_file.read(1_048_576):  # 1MB chunks
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
        """
        Runs the geotagging process.
        """
        # Get images to be tagged
        image_list = _get_images(self.import_dir)

        total_images = len(image_list)

        if self.kml_export:
            kml_gen = ImageKMLGenerator(self.export_dir)

        with ExifToolHelper(executable=self.exec_path) as et:
            for idx, image_fn in enumerate(image_list):
                relative_fn = image_fn.relative_to(self.import_dir)
                exif_data = et.get_metadata(str(image_fn))[0]
                new_exif_tags = copy.copy(self.base_tags)
                try:
                    new_exif_tags |= self.tagger.generate_gps_tags(exif_data,
                                                                   tz_override=self.tz_override)
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
                et.set_tags(files=save_fn, tags=new_exif_tags, params=['-overwrite_original'])
                if self.ifdo_model is not None:
                    self.add_to_ifdo(relative_fn, exif_data, new_exif_tags)
                logger.info("Image %s geotagged and saved to %s", image_fn, save_fn)
                if self.kml_export:
                    try:
                        kml_gen.add_image_point(save_fn)
                    except KeyError as e:
                        logger.error("Missing GPS data in image %s: %s", image_fn, e)
                        self.error_msgs.emit(f"Missing GPS data in image {image_fn}: {e}")
                self.progress.emit(idx, total_images)
        # Save the IFDO model to a file
        if self.ifdo_model is not None:
            ifdo_path = self.export_dir / "ifdo.yml"
            self.ifdo_model.export_ifdo_yaml(str(ifdo_path))
            logger.info("IFDO file saved to %s", ifdo_path)

        # Save KML file if required
        if self.kml_export:
            kml_gen.save()
            logger.info("KML file saved to %s", self.export_dir / 'images.kml')
        self.finished.emit("Finished geotagging images.")

class MainController(QObject):
    """
    Main controller that handles the interaction between the view and the model.
    """
    def __init__(self, app_view: views.MainWindow, model: models.UserInputModel,
                 config: models.ConfigModel, feedback: models.FeedbackModel,
                 exec_path: Optional[str] = None):
        super().__init__()
        self._app_view = app_view
        self._model = model
        self._config = config
        # self._model.importDirectoryChanged.connect(self.countImages)
        self._feedback = feedback
        self._worker = None
        self._workerthread = None
        self._exec_path = exec_path


        # Connect the signals from the view to the model
        self._app_view.inputDirChanged.connect(lambda x: setattr(self._model, 'importDirectory', x))
        self._app_view.gpxFileChanged.connect(lambda x: setattr(self._model, 'gpxFilepath', x))
        self._app_view.gpsPhotoAvailableChanged.connect(
            lambda x: setattr(self._model, 'gpsPhotoAvailable', x))
        self._app_view.gpsPhotoChanged.connect(
            lambda x: setattr(self._model, 'gpsPhotoFilepath', x))
        self._app_view.gpsDateChanged.connect(lambda x: setattr(self._model, 'gpsDate', x))
        self._app_view.gpsTimeChanged.connect(lambda x: setattr(self._model, 'gpsTime', x))
        self._app_view.gpsTimezoneIndexChanged.connect(
            lambda x: setattr(self._model, 'gpsTimezoneIndex', x))
        self._app_view.cameraTimezoneIndexChanged.connect(
            lambda x: setattr(self._model, 'cameraTimezoneIndex', x))
        self._app_view.outputDirChanged.connect(
            lambda x: setattr(self._model, 'exportDirectory', x))
        self._app_view.ifdoExportChanged.connect(lambda x: setattr(self._model, 'ifdoEnable', x))
        self._app_view.imageSetNameChanged.connect(
            lambda x: setattr(self._model, 'imageSetName', x))
        self._app_view.contextChanged.connect(lambda x: setattr(self._model, 'imageContext', x))
        self._app_view.projectNameChanged.connect(lambda x: setattr(self._model, 'projectName', x))
        self._app_view.campaignNameChanged.connect(
            lambda x: setattr(self._model, 'campaignName', x))
        self._app_view.piNameChanged.connect(lambda x: setattr(self._model, 'piName', x))
        self._app_view.piOrcidChanged.connect(lambda x: setattr(self._model, 'piORCID', x))
        self._app_view.collectorNameChanged.connect(
            lambda x: setattr(self._model, 'collectorName', x))
        self._app_view.collectorOrcidChanged.connect(
            lambda x: setattr(self._model, 'collectorORCID', x))
        self._app_view.copyrightOwnerChanged.connect(
            lambda x: setattr(self._model, 'organisation', x))
        self._app_view.licenseChanged.connect(lambda x: setattr(self._model, 'license', x))
        self._app_view.distanceAGChanged.connect(
            lambda x: setattr(self._model, 'distanceAboveGround', x))
        self._app_view.imageObjectiveChanged.connect(
            lambda x: setattr(self._model, 'imageObjective', x))
        self._app_view.imageAbstractChanged.connect(
            lambda x: setattr(self._model, 'imageAbstract', x))
        self._app_view.startProcessingTriggered.connect(self.geotag)
        self._app_view.kmlExportChanged.connect(lambda x: setattr(self._model, 'exportKML', x))
        self._app_view.attributionExportChanged.connect(
            lambda x: setattr(self._model, 'attributionExport', x))

        # Connect internal view logic
        self._app_view.clearFormTriggered.connect(self._app_view.clearForm)
        self._app_view.inputDirChanged.connect(self._app_view.setDefaultPath)
        self._app_view.attributionExportChanged.connect(\
            self._app_view.enableDisableAttributionFields)
        self._app_view.ifdoExportChanged.connect(self._app_view.enableDisableIFDODetails)
        self._app_view.gpsPhotoChanged.connect(self._app_view._image_preview.setFilepath)

        # Connect menu actions
        self._app_view.aboutTriggered.connect(self.show_about)
        self._app_view.documentationTriggered.connect(self._app_view.OpenDocumentationURL)

        # Set up configs into view
        default_window_title = self._app_view.windowTitle()
        self._app_view.setWindowTitle(f"{default_window_title} - v{self._config.version}")
        self._app_view.setTimezoneOptions(self._config.gpsTimezoneOptions)
        if self._config.useWorkaround:
            self._app_view.setTimezoneIndexDefault(15, reset=True)

        # Set up the feedback model into view
        self._feedback.feedbackTextChanged.connect(self._app_view.setFeedbackText)
        self._feedback.progressChanged.connect(self._app_view.setProgress)

    # Slot to start the geotagging process
    @Slot()
    def geotag(self):
        """
        Slot intended to start the geotagging process.
        This method validates the user input, and starts the geotagging worker thread.
        """
        # Manually trigger field signals to update the model
        self._app_view.manuallyTriggerFieldSignals()

        # Clear any previous feedback
        self._feedback.feedbackText = ""
        # Validate the input
        validator = models.UserInputModelValidator()
        self._feedback.feedbackText = "Validating input...\n"
        if not validator.validate(self._model):
            self._feedback.addFeedbackLine("Validation failed")
            for error in validator.latest_errors:
                self._feedback.addFeedbackLine(error)
            return

        # Create the PhotoTransectGPSTagger object
        # Use GPS photo and timestamp only if GPS photo is available
        tz_override = self._config.gpsTimezoneOptions[self._model.cameraTimezoneIndex]\
                          .replace("UTC", "")
        if self._model.gpsPhotoAvailable:
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
            gps_photo_path = self._model.gpsPhotoFilepath.replace("file://", "")
        else:
            jpg_gps_timestamp = None
            gps_photo_path = None

        tagger = PhotoTransectGPSTagger.from_files(
            self._model.gpxFilepath.replace("file://", ""),
            jpg_gps_fn=gps_photo_path,
            jpg_gps_timestamp=jpg_gps_timestamp,
            exiftool_path=self._exec_path,
            tz_override=tz_override
        )
        # Create the IFDO model
        if self._model.ifdoEnable:
            ifdo_model = IFDOModel(image_set_name=self._model.imageSetName,
                                   image_context=self._model.imageContext,
                                   image_project=self._model.projectName,
                                   image_event=self._model.campaignName,
                                   image_pi=(self._model.piName, self._model.piORCID if \
                                             self._model.piORCID != "" else "0000-0000-0000-0000"),
                                   image_creators=[(self._model.collectorName, \
                                                    self._model.collectorORCID if \
                                                        self._model.collectorORCID != "" else \
                                                        "0000-0000-0000-0000")],
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
                                    exec_path=self._exec_path, tz_override=tz_override,
                                    kml_export=self._model.exportKML)

        # Set base tags for the images if attribution export is enabled
        if self._model.attributionExport:
            if self._model.collectorORCID != "":
                collector_str = f"{self._model.collectorName} " + \
                f"(Image collector, ORCID: {self._model.collectorORCID})"
            else:
                collector_str = f"{self._model.collectorName} (Image collector)"
            if self._model.piORCID != "":
                pi_str = f"{self._model.piName} " + \
                f"(Principal Investigator, ORCID: {self._model.piORCID})"
            else:
                pi_str = f"{self._model.piName} (Principal Investigator)"
            self._worker.set_base_tags({
                "Exif:Artist": f"{collector_str}; {pi_str}",
                "Creator": f"{collector_str}; {pi_str}",
                "Copyright": f"{self._model.organisation} (Licensed under {self._model.license})"
            })

        # Move the worker to the thread and connect signals
        self._worker.moveToThread(self._workerthread)
        self._workerthread.started.connect(self._worker.run)
        self._worker.progress.connect(self._feedback.updateProgress)
        self._worker.finished.connect(self._workerthread.quit)
        self._worker.error_msgs.connect(self._feedback.addFeedbackLine)
        self._worker.finished.connect(self._feedback.addFeedbackLine)
        self._worker.finished.connect(self._worker.deleteLater)
        self._workerthread.finished.connect(self._workerthread.deleteLater)

        # This ensures the progress bar fills up once execution completes
        self._workerthread.finished.connect(lambda : self._app_view.setProgress(100))

        # Start worker thread and update the UI
        self._workerthread.start()
        if self._model.gpsPhotoAvailable:
            self._feedback.addFeedbackLine("Geotagging images using GPS photo synchronization...")
        else:
            self._feedback.addFeedbackLine("Geotagging images assuming camera and GPS times "
                                           "are synchronized...")
        self._feedback.addFeedbackLine("Processing images...")

    @Slot()
    def show_about(self):
        """Show the About dialog with version and build information."""
        self._app_view.showAboutDialog(
            version=self._config.version,
            build_hash=self._config.buildHash
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    user_input_model = models.UserInputModel()
    config_model = models.ConfigModel()
    config_model.initialise()
    feedback_model = models.FeedbackModel()

    main_view = views.MainWindow()

    # Determine if we're a package or running as a script
    if getattr(sys, "frozen", False):
        logger.info("Running as a package")
        app_path = Path(sys._MEIPASS) # pylint: disable=protected-access
        if sys.platform == "win32":
            EXIFTOOL_PATH = str(app_path / "bin" / "exiftool.exe")
        else:
            EXIFTOOL_PATH = str(app_path / "bin" / "exiftool")
        # Read the git hash from the build_id.txt file
        build_id_path = app_path / "build_id.txt"
        if build_id_path.exists():
            with open(build_id_path, "r", encoding="utf-8") as f:
                config_model.buildHash = f.read().strip()
            logger.info("Build ID: %s", config_model.buildHash)
        else:
            logger.warning("Build ID file not found.")
        # Read the version from the version.txt file
        version_path = app_path / "version.txt"
        if version_path.exists():
            with open(version_path, "r", encoding="utf-8") as f:
                config_model.version = f.read().strip()
            logger.info("Version: %s", config_model.version)
        else:
            logger.warning("Version file not found.")
    else:
        # Probably developing, safe to assume we're in the development dir
        app_path = Path(os.path.dirname(os.path.realpath(__file__)))
        if sys.platform == "darwin":
            EXIFTOOL_PATH = str(app_path / ".." / "Image-ExifTool-13.29" / "exiftool")
        elif sys.platform == "win32":
            EXIFTOOL_PATH = str(app_path / ".." / "exiftool-13.29_64" / "exiftool.exe")
        else:
            print(sys.platform)
            raise NotImplementedError("This platform is not currently supported")


    controller = MainController(app_view=main_view,
                                model=user_input_model,
                                config=config_model,
                                feedback=feedback_model,
                                exec_path=EXIFTOOL_PATH)

    main_view.show()
    sys.exit(app.exec())

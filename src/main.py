import datetime
import logging
import os
import shutil
import sys
import threading
import zoneinfo
from pathlib import Path

import gpxpy
import piexif
from geotag_pt import PhotoTransectGPSTagger
from PyQt6.QtCore import QObject, QThread, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

import models

logger = logging.getLogger(__name__)



def _get_images(directory: Path):
    extensions = ['.jpg', '.jpeg', '.png']
    if not directory.exists() or not directory.is_dir():
        return []
    file_list = list(directory.rglob("*"))
    return [file for file in file_list if file.suffix.lower() in extensions]

class GeotagWorker(QObject):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal()

    def __init__(self, tagger: PhotoTransectGPSTagger, import_dir: Path, export_dir: Path):
        super().__init__()
        self.tagger = tagger
        self.import_dir = import_dir
        self.export_dir = export_dir
    
    def run(self):
        # Get images to be tagged
        image_list = _get_images(self.import_dir)

        total_images = len(image_list)

        tally = 0

        for image_fn in image_list:
            exif_data = piexif.load(str(image_fn))
            try:
                exif_data = self.tagger.generate_new_exif(exif_data)
            except IndexError as e:
                logger.error(
                    "Image %s not within range of GPX file. Skipping this image.", image_fn
                )
                logger.error(e)
                continue
            except AssertionError as _:
                logger.error(
                    "Image %s does not contain time data. Skipping this image.", image_fn
                )
                continue
            save_fn = self.export_dir / image_fn.relative_to(self.import_dir)
            save_fn.parent.mkdir(parents=True, exist_ok=True)
            if not save_fn.parent.exists():
                logger.error("Failed to create directory %s", save_fn.parent)
                continue
            shutil.copy2(image_fn, save_fn)
            piexif.insert(
                piexif.dump(exif_data), str(save_fn)
            )
            logger.info("Image %s geotagged and saved to %s", image_fn, save_fn)
            tally += 1
            self.progress.emit(tally, total_images)
        self.finished.emit()



class MainController(QObject):
    def __init__(self, model: models.UserInputModel, config: models.ConfigModel, feedback: models.FeedbackModel):
        super().__init__()
        self._model = model
        self._config = config
        self._model.gpxFilepathChanged.connect(self.gpxFileSelected)
        self._model.gpsDateChanged.connect(self.gpsPhotoDateSet)
        self._model.importDirectoryChanged.connect(self.countImages)
        self._feedback = feedback
        self._worker = None
        self._workerthread = None

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
        jpg_gps_timestamp = jpg_gps_timestamp.replace(tzinfo=zoneinfo.ZoneInfo(
            self._config.gpsTimezoneOptions[self._model.gpsTimezoneIndex]))
        tagger = PhotoTransectGPSTagger.from_files(
            self._model.gpxFilepath.replace("file://", ""),
            self._model.gpsPhotoFilepath.replace("file://", ""),
            jpg_gps_timestamp
        )

        # Create new worker thread
        self._workerthread = QThread()
        import_dir = Path(self._model.importDirectory.replace("file://", ""))
        export_dir = Path(self._model.exportDirectory.replace("file://", ""))
        self._worker = GeotagWorker(tagger, import_dir, export_dir)
        self._worker.moveToThread(self._workerthread)
        self._workerthread.started.connect(self._worker.run)
        self._worker.progress.connect(self._feedback.updateProgress)
        self._worker.finished.connect(self._workerthread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._workerthread.finished.connect(self._workerthread.deleteLater)
        self._workerthread.start()
        self._feedback.addFeedbackLine("Geotagging images...\n")
        return True

            
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    user_input_model = models.UserInputModel()
    config_model = models.ConfigModel()
    feedback_model = models.FeedbackModel()
    controller = MainController(user_input_model, config_model, feedback_model)

    # Determine if we're a package or running as a script
    if getattr(sys, "frozen", False):
        app_path = Path(sys._MEIPASS)
    else:
        app_path = Path(os.path.dirname(os.path.realpath(__file__)))

    engine.rootContext().setContextProperty("userInputModel", user_input_model)
    engine.rootContext().setContextProperty("configModel", config_model)
    engine.rootContext().setContextProperty("feedbackModel", feedback_model)
    engine.rootContext().setContextProperty("controller", controller)
    config_model.initialise()
    engine.load((app_path / "main.qml").as_uri())

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

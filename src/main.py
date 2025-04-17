import os
import sys
import threading
from pathlib import Path

import gpxpy
from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

from config_model import ConfigModel
from user_input_model import UserInputModel


class MainController(QObject):
    def __init__(self, model: UserInputModel):
        super().__init__()
        self._model = model
        self._model.gpxFilepathChanged.connect(self.gpxFileSelected)
        self._model.gpsDateChanged.connect(self.gpsPhotoDateSet)
        self._model.importDirectoryChanged.connect(self.countImages)

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
        extensions = ['.jpg', '.jpeg', '.png']
        path = Path(directory.replace("file://", ""))
        if not path.exists() or not path.is_dir():
            return 0
        file_list = list(path.rglob("*"))
        image_list = [file for file in file_list if file.suffix.lower() in extensions]
        return len(image_list)

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    user_input_model = UserInputModel()
    config_model = ConfigModel()
    controller = MainController(user_input_model)

    # Determine if we're a package or running as a script
    if getattr(sys, "frozen", False):
        app_path = Path(sys._MEIPASS)
    else:
        app_path = Path(os.path.dirname(os.path.realpath(__file__)))

    engine.rootContext().setContextProperty("userInputModel", user_input_model)
    engine.rootContext().setContextProperty("configModel", config_model)
    config_model.initialise()
    engine.load((app_path / "main.qml").as_uri())

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

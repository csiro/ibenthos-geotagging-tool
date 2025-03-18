import os
import sys
import threading
import zoneinfo
from pathlib import Path

import gpxpy
from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine


class MainModel(QObject):
    avgLatitudeChanged = pyqtSignal(str)
    avgLongitudeChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._avg_lat = "0.0"
        self._avg_lon = "0.0"

    @pyqtProperty(str, notify=avgLatitudeChanged)
    def averageLatitude(self):
        return self._avg_lat

    @pyqtProperty(str, notify=avgLongitudeChanged)
    def averageLongitude(self):
        return self._avg_lon

    @averageLatitude.setter
    def averageLatitude(self, lat):
        if self._avg_lat != lat:
            self._avg_lat = lat
            self.avgLatitudeChanged.emit(lat)
            print(f"Average latitude: {lat}")

    @averageLongitude.setter
    def averageLongitude(self, lon):
        if self._avg_lon != lon:
            self._avg_lon = lon
            self.avgLongitudeChanged.emit(lon)

    @pyqtSlot(str)
    def updateFilePath(self, path):
        self.filePath = path

    @pyqtSlot(str)
    def onGpxFileSelected(self, path):
        threading.Thread(target=self._process_gpx_file, args=(path,)).start()

    def _process_gpx_file(self, path):
        # Open the GPX file and read the data
        with open(path.replace("file://", ""), "r") as file:
            gpx = gpxpy.parse(file)

        # Extract the data from the GPX file
        avg_lat = 0
        avg_lon = 0
        avg_ele = 0
        count = 0
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    avg_lat += point.latitude
                    avg_lon += point.longitude
                    avg_ele += point.elevation
                    count += 1
        avg_lat /= count
        avg_lon /= count
        avg_ele /= count
        # print(f"Average latitude: {avg_lat:.08f}")
        self.averageLatitude = f"{avg_lat:.08f}"
        # print(f"Average longitude: {avg_lon:.08f}")
        self.averageLongitude = f"{avg_lon:.08f}"
        # print(f"Average elevation: {avg_ele:.02f}")

class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    model = MainModel()
    controller = MainController(model)

    # Determine if we're a package or running as a script
    if getattr(sys, "frozen", False):
        app_path = Path(sys._MEIPASS)
    else:
        app_path = Path(os.path.dirname(os.path.realpath(__file__)))

    engine.rootContext().setContextProperty("mainModel", model)
    engine.load((app_path / "main.qml").as_uri())

    if not engine.rootObjects():
        sys.exit(-1)
    
    timezones = sorted(zoneinfo.available_timezones())

    engine.rootObjects()[0].setProperty("timezones", timezones)

    sys.exit(app.exec())

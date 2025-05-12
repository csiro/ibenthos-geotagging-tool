
import zoneinfo

from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal


class ConfigModel(QObject):
    gpsTimezoneOptionsChanged = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._gps_timezone_options = []

    @pyqtProperty(list, notify=gpsTimezoneOptionsChanged)
    def gpsTimezoneOptions(self):
        return self._gps_timezone_options

    @gpsTimezoneOptions.setter
    def gpsTimezoneOptions(self, options):
        if self._gps_timezone_options != options:
            self._gps_timezone_options = options
            self.gpsTimezoneOptionsChanged.emit(options)

    def initialise(self):
        self.gpsTimezoneOptions = sorted(zoneinfo.available_timezones())
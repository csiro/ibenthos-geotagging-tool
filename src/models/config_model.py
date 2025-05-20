
import zoneinfo
from datetime import timedelta, tzinfo

from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal


class ConfigModel(QObject):
    gpsTimezoneOptionsChanged = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._gps_timezone_options = []
        self._use_workaround = False

    @pyqtProperty(list, notify=gpsTimezoneOptionsChanged)
    def gpsTimezoneOptions(self):
        return self._gps_timezone_options

    @gpsTimezoneOptions.setter
    def gpsTimezoneOptions(self, options):
        if self._gps_timezone_options != options:
            self._gps_timezone_options = options
            self.gpsTimezoneOptionsChanged.emit(options)


    @pyqtProperty(bool)
    def useWorkaround(self):
        return self._use_workaround

    def initialise(self):
        self.gpsTimezoneOptions = sorted(zoneinfo.available_timezones())

        # Workaround for pyinstaller issue importing zoneinfo
        if len(self.gpsTimezoneOptions) == 0:
            self.gpsTimezoneOptions = ['UTC-12:00', 'UTC-11:00', 'UTC-10:00', 'UTC-09:30', 'UTC-09:00',
                                    'UTC-08:00', 'UTC-07:00', 'UTC-06:00', 'UTC-05:00', 'UTC-04:00',
                                    'UTC-03:30', 'UTC-03:00', 'UTC-02:30', 'UTC-02:00', 'UTC-01:00',
                                    'UTC+00:00', 'UTC+01:00', 'UTC+02:00', 'UTC+03:00', 'UTC+03:30',
                                    'UTC+04:00', 'UTC+04:30', 'UTC+05:00', 'UTC+05:30', 'UTC+05:45',
                                    'UTC+06:00', 'UTC+06:30', 'UTC+07:00', 'UTC+08:00', 'UTC+08:45',
                                    'UTC+09:00', 'UTC+09:30', 'UTC+10:00', 'UTC+10:30', 'UTC+11:00',
                                    'UTC+12:00', 'UTC+12:45', 'UTC+13:00', 'UTC+13:45', 'UTC+14:00']
            self._use_workaround = True

class TimezoneWorkaround(tzinfo):
    '''
    A workaround for the issue with PyInstaller not being able to find the zoneinfo module.
    This class is used to create a timezone object from a string in the format 'UTC±HH:MM'.
    '''
    def __init__(self, name):
        self._tzname = name
        time = name.replace('UTC', '').split(':')
        self._utcoffset = timedelta(hours=int(time[0]), minutes=int(time[1]))
        self._dst = timedelta(0)

    def utcoffset(self, dt):
        return self._utcoffset

    def dst(self, dt):
        return self._dst

    def tzname(self, dt):
        return self._tzname

    def fromutc(self, dt):
        return dt + self.utcoffset(dt)

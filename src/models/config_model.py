"""
config_model.py: This module defines a configuration model for the application.
It includes properties for GPS timezone options, build hash and version.

Copyright (c) 2025
Commonwealth Scientific and Industrial Research Organisation (CSIRO)
ABN 41 687 119 230

Author: Brendan Do <brendan.do@csiro.au>
"""
from PySide6.QtCore import Property, QObject, Signal


class ConfigModel(QObject):
    """
    This class defines a configuration model for the application.
    It includes properties for GPS timezone options, build hash, version, and timezones.
    """
    # pylint: disable=invalid-name
    # Camel case to comply with pyside6 naming conventions

    # pylint: disable=missing-function-docstring
    # Setters and getters are self-explanatory and do not require additional documentation

    gpsTimezoneOptionsChanged = Signal(list)

    def __init__(self):
        super().__init__()
        self._gps_timezone_options = []
        self._build_hash = "0"
        self._version = "0.0.0"

    @Property(list, notify=gpsTimezoneOptionsChanged)
    def gpsTimezoneOptions(self):
        return self._gps_timezone_options

    @gpsTimezoneOptions.setter
    def gpsTimezoneOptions(self, options):
        self._gps_timezone_options = options
        self.gpsTimezoneOptionsChanged.emit(options)

    @Property(str)
    def buildHash(self):
        return self._build_hash

    @buildHash.setter
    def buildHash(self, value):
        if self._build_hash != value:
            self._build_hash = value

    @Property(str)
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if self._version != value:
            self._version = value

"""
user_input_model.py: Data model for user input in the iBenthos Geotagging Tool application.
This module defines the UserInputModel class, which manages user input data and provides validation
methods.

Copyright (c) 2025
Commonwealth Scientific and Industrial Research Organisation (CSIRO)
ABN 41 687 119 230

Author: Brendan Do <brendan.do@csiro.au>
"""
import datetime
import re
from pathlib import Path

from PySide6.QtCore import Property, QObject, Signal, Slot


class UserInputModel(QObject):
    """
    Data model for user input in the iBenthos Geotagging Tool application.
    This class provides properties for user input fields and emits signals when a property changes.
    It also provides a method to clear all user input fields to their default values.
    """
    # pylint: disable=invalid-name
    # Camel case to comply with pyside6 naming conventions

    # pylint: disable=missing-function-docstring
    # Setters and getters are self-explanatory and do not require additional documentation

    importDirectoryChanged = Signal(str)
    gpxFilepathChanged = Signal(str)
    gpsPhotoAvailableChanged = Signal(bool)
    gpsPhotoFilepathChanged = Signal(str)
    gpsDateChanged = Signal(str)
    gpsTimeChanged = Signal(str)
    gpsTimezoneIndexChanged = Signal(int)
    cameraTimezoneIndexChanged = Signal(int)
    exportDirectoryChanged = Signal(str)
    ifdoEnableChanged = Signal(bool)
    imageSetNameChanged = Signal(str)
    imageContextChanged = Signal(str)
    projectNameChanged = Signal(str)
    eventNameChanged = Signal(str)
    piNameChanged = Signal(str)
    piORCIDChanged = Signal(str)
    collectorNameChanged = Signal(str)
    collectorORCIDChanged = Signal(str)
    organisationChanged = Signal(str)
    licenseChanged = Signal(str)
    distanceAboveGroundChanged = Signal(str)
    imageAbstractChanged = Signal(str)
    exportKMLChanged = Signal(bool)
    attributionExportChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        self._import_dir = ""
        self._gpx_filepath = ""
        self._gps_photo_available = False
        self._gps_photo_filepath = ""
        self._gps_date = ""
        self._gps_time = ""
        self._gps_timezone_index = 0
        self._camera_timezone_index = 0
        self._export_dir = ""
        self._ifdo_enable = False
        self._image_set_name = ""
        self._image_context = ""
        self._project_name = ""
        self._event_name = ""
        self._pi_name = ""
        self._pi_orcid = ""
        self._collector_name = ""
        self._collector_orcid = ""
        self._organisation = ""
        self._license = "CC BY 4.0"
        self._distance_above_ground = ""
        self._image_abstract = ""
        self._kml_enable = False
        self._attribution_export = False

    @Property(str, notify=importDirectoryChanged)
    def importDirectory(self):
        return self._import_dir

    @importDirectory.setter
    def importDirectory(self, directory):
        if self._import_dir != directory:
            self._import_dir = directory
            self.importDirectoryChanged.emit(directory)

    @Property(str, notify=gpxFilepathChanged)
    def gpxFilepath(self):
        return self._gpx_filepath

    @gpxFilepath.setter
    def gpxFilepath(self, path):
        if self._gpx_filepath != path:
            self._gpx_filepath = path
            self.gpxFilepathChanged.emit(path)

    @Property(bool, notify=gpsPhotoAvailableChanged)
    def gpsPhotoAvailable(self):
        return self._gps_photo_available

    @gpsPhotoAvailable.setter
    def gpsPhotoAvailable(self, available):
        if self._gps_photo_available != available:
            self._gps_photo_available = available
            self.gpsPhotoAvailableChanged.emit(available)

    @Property(str, notify=gpsPhotoFilepathChanged)
    def gpsPhotoFilepath(self):
        return self._gps_photo_filepath

    @gpsPhotoFilepath.setter
    def gpsPhotoFilepath(self, path):
        if self._gps_photo_filepath != path:
            self._gps_photo_filepath = path
            self.gpsPhotoFilepathChanged.emit(path)

    @Property(str, notify=gpsDateChanged)
    def gpsDate(self):
        return self._gps_date

    @gpsDate.setter
    def gpsDate(self, date):
        if self._gps_date != date:
            self._gps_date = date
            self.gpsDateChanged.emit(date)

    @Property(str, notify=gpsTimeChanged)
    def gpsTime(self):
        return self._gps_time

    @gpsTime.setter
    def gpsTime(self, time):
        if self._gps_time != time:
            self._gps_time = time
            self.gpsTimeChanged.emit(time)

    @Property(int, notify=gpsTimezoneIndexChanged)
    def gpsTimezoneIndex(self):
        return self._gps_timezone_index

    @gpsTimezoneIndex.setter
    def gpsTimezoneIndex(self, timezone):
        if self._gps_timezone_index != timezone:
            self._gps_timezone_index = timezone
            self.gpsTimezoneIndexChanged.emit(timezone)

    @Property(int, notify=cameraTimezoneIndexChanged)
    def cameraTimezoneIndex(self):
        return self._camera_timezone_index

    @cameraTimezoneIndex.setter
    def cameraTimezoneIndex(self, timezone):
        if self._camera_timezone_index != timezone:
            self._camera_timezone_index = timezone
            self.cameraTimezoneIndexChanged.emit(timezone)

    @Property(str, notify=exportDirectoryChanged)
    def exportDirectory(self):
        return self._export_dir

    @exportDirectory.setter
    def exportDirectory(self, directory):
        if self._export_dir != directory:
            self._export_dir = directory
            self.exportDirectoryChanged.emit(directory)

    @Property(bool, notify=ifdoEnableChanged)
    def ifdoEnable(self):
        return self._ifdo_enable

    @ifdoEnable.setter
    def ifdoEnable(self, enable):
        if self._ifdo_enable != enable:
            self._ifdo_enable = enable
            self.ifdoEnableChanged.emit(enable)

    @Property(str, notify=imageSetNameChanged)
    def imageSetName(self):
        return self._image_set_name

    @imageSetName.setter
    def imageSetName(self, image_set_name):
        if self._image_set_name != image_set_name:
            self._image_set_name = image_set_name
            self.imageSetNameChanged.emit(image_set_name)

    @Property(str, notify=imageContextChanged)
    def imageContext(self):
        return self._image_context

    @imageContext.setter
    def imageContext(self, image_context):
        if self._image_context != image_context:
            self._image_context = image_context
            self.imageContextChanged.emit(image_context)

    @Property(str, notify=projectNameChanged)
    def projectName(self):
        return self._project_name

    @projectName.setter
    def projectName(self, name):
        if self._project_name != name:
            self._project_name = name
            self.projectNameChanged.emit(name)

    @Property(str, notify=eventNameChanged)
    def eventName(self):
        return self._event_name

    @eventName.setter
    def eventName(self, name):
        if self._event_name != name:
            self._event_name = name
            self.eventNameChanged.emit(name)

    @Property(str, notify=piNameChanged)
    def piName(self):
        return self._pi_name

    @piName.setter
    def piName(self, name):
        if self._pi_name != name:
            self._pi_name = name
            self.piNameChanged.emit(name)

    @Property(str, notify=piORCIDChanged)
    def piORCID(self):
        return self._pi_orcid

    @piORCID.setter
    def piORCID(self, orcid):
        if self._pi_orcid != orcid:
            self._pi_orcid = orcid
            self.piORCIDChanged.emit(orcid)

    @Property(str, notify=collectorNameChanged)
    def collectorName(self):
        return self._collector_name

    @collectorName.setter
    def collectorName(self, name):
        if self._collector_name != name:
            self._collector_name = name
            self.collectorNameChanged.emit(name)

    @Property(str, notify=collectorORCIDChanged)
    def collectorORCID(self):
        return self._collector_orcid

    @collectorORCID.setter
    def collectorORCID(self, orcid):
        if self._collector_orcid != orcid:
            self._collector_orcid = orcid
            self.collectorORCIDChanged.emit(orcid)

    @Property(str, notify=organisationChanged)
    def organisation(self):
        return self._organisation

    @organisation.setter
    def organisation(self, org):
        if self._organisation != org:
            self._organisation = org
            self.organisationChanged.emit(org)

    @Property(str, notify=licenseChanged)
    def license(self):
        return self._license

    @license.setter
    def license(self, new_license):
        if self._license != new_license:
            self._license = new_license
            self.licenseChanged.emit(new_license)

    @Property(str, notify=distanceAboveGroundChanged)
    def distanceAboveGround(self):
        return self._distance_above_ground

    @distanceAboveGround.setter
    def distanceAboveGround(self, distance):
        if self._distance_above_ground != distance:
            self._distance_above_ground = distance
            self.distanceAboveGroundChanged.emit(distance)

    @Property(str, notify=imageAbstractChanged)
    def imageAbstract(self):
        return self._image_abstract

    @imageAbstract.setter
    def imageAbstract(self, abstract):
        if self._image_abstract != abstract:
            self._image_abstract = abstract
            self.imageAbstractChanged.emit(abstract)

    @Property(bool, notify=exportKMLChanged)
    def exportKML(self):
        return self._kml_enable

    @exportKML.setter
    def exportKML(self, kml_enable):
        if self._kml_enable != kml_enable:
            self._kml_enable = kml_enable
            self.exportKMLChanged.emit(kml_enable)

    @Property(bool, notify=attributionExportChanged)
    def attributionExport(self):
        return self._attribution_export

    @attributionExport.setter
    def attributionExport(self, attribution_enable):
        if self._attribution_export != attribution_enable:
            self._attribution_export = attribution_enable
            self.attributionExportChanged.emit(attribution_enable)

    @Slot()
    def clearForm(self):
        """
        Reset the UserInputModel to its default state.
        This method clears all the user input fields to their default values.
        """
        self.importDirectory("")
        self.gpxFilepath("")
        self.gpsPhotoAvailable(False)
        self.gpsPhotoFilepath("")
        self.gpsDate("")
        self.gpsTime("")
        self.gpsTimezoneIndex(0)
        self.cameraTimezoneIndex(0)
        self.exportDirectory("")
        self.ifdoEnable(False)
        self.imageSetName("")
        self.imageContext("")
        self.projectName("")
        self.eventName("")
        self.piName("")
        self.piORCID("")
        self.collectorName("")
        self.collectorORCID("")
        self.organisation("")
        self.license("CC BY 4.0")
        self.distanceAboveGround("")
        self.imageAbstract("")
        self.exportKML("")
        self.attributionExport("")

class UserInputModelValidator:
    """
    Validator for the UserInputModel class.
    """
    def __init__(self):
        self.latest_errors = []

    def validate(self, model: UserInputModel) -> bool:
        """
        Validate the user input model.
        This method checks all the required fields and returns True if all validations pass,
        otherwise returns False and sets the latest_errors attribute with the error messages.
        Args:
            model (UserInputModel): The user input model to validate.
        Returns:
            bool: True if the model is valid, False otherwise.
        Sets:
            latest_errors (list): A list of error messages if validation fails, empty if validation 
                                  passes
        """
        main_validators = {
            self._validate_import_directory : [model.importDirectory],
            self._validate_gpx_file : [model.gpxFilepath],
            self._validate_gps_photo_available : [model.gpsPhotoAvailable],
            self._validate_gps_photo_file : [model.gpsPhotoAvailable, model.gpsPhotoFilepath],
            self._validate_gps_date : [model.gpsPhotoAvailable, model.gpsDate],
            self._validate_gps_time : [model.gpsPhotoAvailable, model.gpsTime],
            self._validate_gps_timezone : [model.gpsTimezoneIndex],
            self._validate_camera_timezone : [model.cameraTimezoneIndex],
            self._validate_output_directory : [model.exportDirectory],
            self._validate_export_kml: [model.exportKML],
            self._validate_attribution_export: [model.attributionExport],
            self._validate_pi_name : [model.attributionExport, model.piName],
            self._validate_pi_orcid : [model.attributionExport, model.piORCID],
            self._validate_collectors_name : [model.attributionExport, model.collectorName],
            self._validate_collectors_orcid : [model.attributionExport, model.collectorORCID],
            self._validate_organisation : [model.attributionExport, model.organisation],
            self._validate_license : [model.attributionExport, model.license],
            self._validate_ifdo_enable : [model.ifdoEnable],
            self._validate_image_set_name : [model.ifdoEnable, model.imageSetName],
            self._validate_image_context : [model.ifdoEnable, model.imageContext],
            self._validate_project_name : [model.ifdoEnable, model.projectName],
            self._validate_event_name : [model.ifdoEnable, model.eventName],
            self._validate_distance_above_ground : [model.ifdoEnable, model.distanceAboveGround],
            self._validate_image_abstract : [model.ifdoEnable, model.imageAbstract],
            self._validate_input_path_not_output_path: [model.importDirectory,
                                                        model.exportDirectory],
        }
        errors = list({x(*y) for x, y in main_validators.items()})
        if len(errors) > 1:
            errors.remove(None)
            self.latest_errors = errors
            return False
        self.latest_errors = []
        return True

    @staticmethod
    def _validate_import_directory(import_dir: str) -> str | None:
        if import_dir == "":
            return "Import directory is empty"
        path = Path(import_dir.replace("file://", ""))
        if not path.exists():
            return "Import directory does not exist"
        if not path.is_dir():
            return "Import directory is not a directory"
        return None

    @staticmethod
    def _validate_gpx_file(gpx_fp: str) -> str | None:
        if gpx_fp == "":
            return "GPX file path is empty"
        path = Path(gpx_fp.replace("file://", ""))
        if not path.exists():
            return "GPX file does not exist"
        if not path.is_file():
            return "GPX file is not a file"
        return None

    @staticmethod
    def _validate_gps_photo_available(_: bool) -> str | None:
        return None

    @staticmethod
    def _validate_gps_photo_file(gps_photo_available: bool, gps_photo_fp: str) -> str | None:
        if not gps_photo_available:
            return None
        if gps_photo_fp == "":
            return "GPS photo file path is empty"
        path = Path(gps_photo_fp.replace("file://", ""))
        if not path.exists():
            return "GPS photo file does not exist"
        if not path.is_file():
            return "GPS photo file is not a file"
        return None

    @staticmethod
    def _validate_gps_date(gps_photo_available: bool, gps_date: str) -> str | None:
        if not gps_photo_available:
            return None
        if gps_date == "":
            return "GPS Date field is empty"
        try:
            datetime.date.fromisoformat(gps_date)
        except ValueError:
            return "GPS Date field is not a valid date"
        return None

    @staticmethod
    def _validate_gps_time(gps_photo_available: bool, gps_time: str) -> str | None:
        if not gps_photo_available:
            return None
        if gps_time == "":
            return "GPS Time field is empty"
        try:
            datetime.time.fromisoformat(gps_time)
        except ValueError:
            return "GPS Time field is not a valid time"
        return None

    @staticmethod
    def _validate_gps_timezone(gps_tz: str) -> str | None:
        if gps_tz < 0:
            return "GPS Timezone field is empty"
        return None

    @staticmethod
    def _validate_camera_timezone(camera_tz: str) -> str | None:
        if camera_tz < 0:
            return "Camera Timezone field is empty"
        return None

    @staticmethod
    def _validate_output_directory(output_dir: str) -> str | None:
        if output_dir == "":
            return "Export directory is empty"
        path = Path(output_dir.replace("file://", ""))
        if not path.exists():
            return "Export directory does not exist"
        if not path.is_dir():
            return "Export directory is not a directory"
        return None

    @staticmethod
    def _validate_export_kml(_: bool) -> str | None:
        return None

    @staticmethod
    def _validate_attribution_export(_: bool) -> str | None:
        return None

    @staticmethod
    def _validate_pi_name(attr_enable: bool, pi_name: str) -> str | None:
        if attr_enable and pi_name == "":
            return "PI name is empty"
        return None

    @staticmethod
    def _validate_pi_orcid(attr_enable: bool, pi_orcid: str) -> str | None:
        if attr_enable and pi_orcid != "":
            # ensure that ORCID is correct format
            if not re.match(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$", pi_orcid):
                return "Principal Investigator ORCID is not in the correct format"
        return None

    @staticmethod
    def _validate_collectors_name(attr_enable: bool, collectors_name: str) -> str | None:
        if attr_enable and collectors_name == "":
            return "Collector's name is empty"
        return None

    @staticmethod
    def _validate_collectors_orcid(attr_enable: bool, collectors_orcid: str) -> str | None:
        if attr_enable and collectors_orcid != "":
            # ensure that ORCID is correct format
            if not re.match(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$", collectors_orcid):
                return "Collector's ORCID is not in the correct format"
        return None

    @staticmethod
    def _validate_organisation(attr_enable: bool, organisation: str) -> str | None:
        if attr_enable and organisation == "":
            return "Copyright owner is empty"
        return None

    @staticmethod
    def _validate_license(attr_enable: bool, license_str: str) -> str | None:
        if attr_enable and license_str == "":
            return "License is empty"
        return None

    @staticmethod
    def _validate_ifdo_enable(_: bool) -> str | None:
        return None

    @staticmethod
    def _validate_image_set_name(ifdo_enable: bool, image_set_name: str) -> str | None:
        if ifdo_enable and image_set_name == "":
            return "Image set name is empty"
        return None

    @staticmethod
    def _validate_image_context(ifdo_enable: bool, image_context: str) -> str | None:
        if ifdo_enable and image_context == "":
            return "Image context is empty"
        return None

    @staticmethod
    def _validate_project_name(ifdo_enable: bool, project_name: str) -> str | None:
        if ifdo_enable and project_name == "":
            return "Project name is empty"
        return None

    @staticmethod
    def _validate_event_name(ifdo_enable: bool, event_name: str) -> str | None:
        if ifdo_enable and event_name == "":
            return "Event name is empty"
        return None

    @staticmethod
    def _validate_distance_above_ground(ifdo_enable: bool, distance: str) -> str | None:
        if ifdo_enable:
            if distance == "":
                return "Distance above ground is empty"
            try:
                float(distance)
            except ValueError:
                return "Distance above ground is not a number"
        return None

    @staticmethod
    def _validate_image_abstract(ifdo_enable: bool, image_abstract: str) -> str | None:
        if ifdo_enable and image_abstract == "":
            return "Image abstract is empty"
        return None

    @staticmethod
    def _validate_input_path_not_output_path(input_path: str, output_path: str) -> str | None:
        if input_path == output_path:
            return "Input directory and output directory cannot be the same"
        return None

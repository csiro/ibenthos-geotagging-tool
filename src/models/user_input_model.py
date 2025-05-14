
import datetime
import re
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot


class UserInputModel(QObject):
    importDirectoryChanged = pyqtSignal(str)
    gpxFilepathChanged = pyqtSignal(str)
    gpsPhotoFilepathChanged = pyqtSignal(str)
    gpsDateChanged = pyqtSignal(str)
    gpsTimeChanged = pyqtSignal(str)
    gpsTimezoneIndexChanged = pyqtSignal(int)
    exportDirectoryChanged = pyqtSignal(str)
    ifdoEnableChanged = pyqtSignal(bool)
    imageSetNameChanged = pyqtSignal(str)
    imageContextChanged = pyqtSignal(str)
    projectNameChanged = pyqtSignal(str)
    campaignNameChanged = pyqtSignal(str)
    piNameChanged = pyqtSignal(str)
    piORCIDChanged = pyqtSignal(str)
    collectorNameChanged = pyqtSignal(str)
    collectorORCIDChanged = pyqtSignal(str)
    organisationChanged = pyqtSignal(str)
    licenseChanged = pyqtSignal(str)
    distanceAboveGroundChanged = pyqtSignal(str)
    imageObjectiveChanged = pyqtSignal(str)
    imageAbstractChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._import_dir = ""
        self._gpx_filepath = ""
        self._gps_photo_filepath = ""
        self._gps_date = ""
        self._gps_time = ""
        self._gps_timezone_index = 0
        self._export_dir = ""
        self._ifdo_enable = False
        self._image_set_name = ""
        self._image_context = ""
        self._project_name = ""
        self._campaign_name = ""
        self._pi_name = ""
        self._pi_orcid = ""
        self._collector_name = ""
        self._collector_orcid = ""
        self._organisation = ""
        self._license = ""
        self._distance_above_ground = ""
        self._image_objective = ""
        self._image_abstract = ""

    @pyqtProperty(str, notify=importDirectoryChanged)
    def importDirectory(self):
        return self._import_dir

    @importDirectory.setter
    def importDirectory(self, directory):
        if self._import_dir != directory:
            self._import_dir = directory
            self.importDirectoryChanged.emit(directory)

    @pyqtProperty(str, notify=gpxFilepathChanged)
    def gpxFilepath(self):
        return self._gpx_filepath

    @gpxFilepath.setter
    def gpxFilepath(self, path):
        if self._gpx_filepath != path:
            self._gpx_filepath = path
            self.gpxFilepathChanged.emit(path)

    @pyqtProperty(str, notify=gpsPhotoFilepathChanged)
    def gpsPhotoFilepath(self):
        return self._gps_photo_filepath

    @gpsPhotoFilepath.setter
    def gpsPhotoFilepath(self, path):
        if self._gps_photo_filepath != path:
            self._gps_photo_filepath = path
            self.gpsPhotoFilepathChanged.emit(path)

    @pyqtProperty(str, notify=gpsDateChanged)
    def gpsDate(self):
        return self._gps_date

    @gpsDate.setter
    def gpsDate(self, date):
        if self._gps_date != date:
            self._gps_date = date
            self.gpsDateChanged.emit(date)

    @pyqtProperty(str, notify=gpsTimeChanged)
    def gpsTime(self):
        return self._gps_time

    @gpsTime.setter
    def gpsTime(self, time):
        if self._gps_time != time:
            self._gps_time = time
            self.gpsTimeChanged.emit(time)

    @pyqtProperty(int, notify=gpsTimezoneIndexChanged)
    def gpsTimezoneIndex(self):
        return self._gps_timezone_index

    @gpsTimezoneIndex.setter
    def gpsTimezoneIndex(self, timezone):
        if self._gps_timezone_index != timezone:
            self._gps_timezone_index = timezone
            self.gpsTimezoneIndexChanged.emit(timezone)

    @pyqtProperty(str, notify=exportDirectoryChanged)
    def exportDirectory(self):
        return self._export_dir

    @exportDirectory.setter
    def exportDirectory(self, directory):
        if self._export_dir != directory:
            self._export_dir = directory
            self.exportDirectoryChanged.emit(directory)

    @pyqtProperty(bool, notify=ifdoEnableChanged)
    def ifdoEnable(self):
        return self._ifdo_enable

    @ifdoEnable.setter
    def ifdoEnable(self, enable):
        if self._ifdo_enable != enable:
            self._ifdo_enable = enable
            self.ifdoEnableChanged.emit(enable)

    @pyqtProperty(str, notify=imageSetNameChanged)
    def imageSetName(self):
        return self._image_set_name

    @imageSetName.setter
    def imageSetName(self, image_set_name):
        if self._image_set_name != image_set_name:
            self._image_set_name = image_set_name
            self.imageSetNameChanged.emit(image_set_name)

    @pyqtProperty(str, notify=imageContextChanged)
    def imageContext(self):
        return self._image_context

    @imageContext.setter
    def imageContext(self, image_context):
        if self._image_context != image_context:
            self._image_context = image_context
            self.imageContextChanged.emit(image_context)

    @pyqtProperty(str, notify=projectNameChanged)
    def projectName(self):
        return self._project_name

    @projectName.setter
    def projectName(self, name):
        if self._project_name != name:
            self._project_name = name
            self.projectNameChanged.emit(name)

    @pyqtProperty(str, notify=campaignNameChanged)
    def campaignName(self):
        return self._campaign_name

    @campaignName.setter
    def campaignName(self, name):
        if self._campaign_name != name:
            self._campaign_name = name
            self.campaignNameChanged.emit(name)

    @pyqtProperty(str, notify=piNameChanged)
    def piName(self):
        return self._pi_name

    @piName.setter
    def piName(self, name):
        if self._pi_name != name:
            self._pi_name = name
            self.piNameChanged.emit(name)

    @pyqtProperty(str, notify=piORCIDChanged)
    def piORCID(self):
        return self._pi_orcid

    @piORCID.setter
    def piORCID(self, orcid):
        if self._pi_orcid != orcid:
            self._pi_orcid = orcid
            self.piORCIDChanged.emit(orcid)

    @pyqtProperty(str, notify=collectorNameChanged)
    def collectorName(self):
        return self._collector_name

    @collectorName.setter
    def collectorName(self, name):
        if self._collector_name != name:
            self._collector_name = name
            self.collectorNameChanged.emit(name)

    @pyqtProperty(str, notify=collectorORCIDChanged)
    def collectorORCID(self):
        return self._collector_orcid

    @collectorORCID.setter
    def collectorORCID(self, orcid):
        if self._collector_orcid != orcid:
            self._collector_orcid = orcid
            self.collectorORCIDChanged.emit(orcid)

    @pyqtProperty(str, notify=organisationChanged)
    def organisation(self):
        return self._organisation

    @organisation.setter
    def organisation(self, org):
        if self._organisation != org:
            self._organisation = org
            self.organisationChanged.emit(org)

    @pyqtProperty(str, notify=licenseChanged)
    def license(self):
        return self._license

    @license.setter
    def license(self, new_license):
        if self._license != new_license:
            self._license = new_license
            self.licenseChanged.emit(new_license)

    @pyqtProperty(str, notify=distanceAboveGroundChanged)
    def distanceAboveGround(self):
        return self._distance_above_ground

    @distanceAboveGround.setter
    def distanceAboveGround(self, distance):
        if self._distance_above_ground != distance:
            self._distance_above_ground = distance
            self.distanceAboveGroundChanged.emit(distance)

    @pyqtProperty(str, notify=imageObjectiveChanged)
    def imageObjective(self):
        return self._image_objective

    @imageObjective.setter
    def imageObjective(self, image_objective):
        if self._image_objective != image_objective:
            self._image_objective = image_objective
            self.imageObjectiveChanged.emit(image_objective)

    @pyqtProperty(str, notify=imageAbstractChanged)
    def imageAbstract(self):
        return self._image_abstract

    @imageAbstract.setter
    def imageAbstract(self, abstract):
        if self._image_abstract != abstract:
            self._image_abstract = abstract
            self.imageAbstractChanged.emit(abstract)

    @pyqtSlot()
    def clearForm(self):
        self.importDirectory = ""
        self.gpxFilepath = ""
        self.gpsPhotoFilepath = ""
        self.gpsDate = ""
        self.gpsTime = ""
        self.gpsTimezoneIndex = 0
        self.exportDirectory = ""
        self.ifdoEnable = False
        self.imageSetName = ""
        self.imageContext = ""
        self.projectName = ""
        self.campaignName = ""
        self.piName = ""
        self.piORCID = ""
        self.collectorName = ""
        self.collectorORCID = ""
        self.organisation = ""
        self.license = ""
        self.distanceAboveGround = ""
        self.imageObjective = ""
        self.imageAbstract = ""

    @pyqtSlot(result=bool)
    def validateForm(self):
        validator = UserInputModelValidator()
        return validator.validate(self)

class UserInputModelValidator:
    def __init__(self):
        self.latest_errors = []

    def validate(self, model: UserInputModel) -> bool:
        main_validators = {
            self._validate_import_directory : [model.importDirectory],
            self._validate_gpx_file : [model.gpxFilepath],
            self._validate_gps_photo_file : [model.gpsPhotoFilepath],
            self._validate_gps_date : [model.gpsDate],
            self._validate_gps_time : [model.gpsTime],
            self._validate_gps_timezone : [model.gpsTimezoneIndex],
            self._validate_output_directory : [model.exportDirectory],
            self._validate_ifdo_enable : [model.ifdoEnable],
            self._validate_image_set_name : [model.ifdoEnable, model.imageSetName],
            self._validate_image_context : [model.ifdoEnable, model.imageContext],
            self._validate_project_name : [model.ifdoEnable, model.projectName],
            self._validate_campaign_name : [model.ifdoEnable, model.campaignName],
            self._validate_pi_name : [model.ifdoEnable, model.piName],
            self._validate_pi_orcid : [model.ifdoEnable, model.piORCID],
            self._validate_collectors_name : [model.ifdoEnable, model.collectorName],
            self._validate_collectors_orcid : [model.ifdoEnable, model.collectorORCID],
            self._validate_organisation : [model.ifdoEnable, model.organisation],
            self._validate_license : [model.ifdoEnable, model.license],
            self._validate_distance_above_ground : [model.ifdoEnable, model.distanceAboveGround],
            self._validate_image_objective = [model.ifdoEnable, model.imageObjective],
            self._validate_image_abstract: [model.ifdoEnable, model.imageAbstract],
        }
        errors = list({x(*y) for x, y in main_validators.items()})
        if len(errors) > 1:
            errors.remove(None)
            self.latest_errors = errors
            return False
        else:
            self.latest_errors = []
            return True

    @staticmethod
    def _validate_import_directory(import_dir: str) -> Optional[str]:
        if import_dir == "":
            return "Import directory is empty"
        path = Path(import_dir.replace("file://", ""))
        if not path.exists():
            return "Import directory does not exist"
        if not path.is_dir():
            return "Import directory is not a directory"
        return None

    @staticmethod
    def _validate_gpx_file(gpx_fp: str) -> Optional[str]:
        if gpx_fp == "":
            return "GPX file path is empty"
        path = Path(gpx_fp.replace("file://", ""))
        if not path.exists():
            return "GPX file does not exist"
        if not path.is_file():
            return "GPX file is not a file"
        return None

    @staticmethod
    def _validate_gps_photo_file(gps_photo_fp: str) -> Optional[str]:
        if gps_photo_fp == "":
            return "GPS photo file path is empty"
        path = Path(gps_photo_fp.replace("file://", ""))
        if not path.exists():
            return "GPS photo file does not exist"
        if not path.is_file():
            return "GPS photo file is not a file"
        return None

    @staticmethod
    def _validate_gps_date(gps_date: str) -> Optional[str]:
        if gps_date == "":
            return "GPS Date field is empty"
        try:
            datetime.date.fromisoformat(gps_date)
        except ValueError:
            return "GPS Date field is not a valid date"
        return None

    @staticmethod
    def _validate_gps_time(gps_time: str) -> Optional[str]:
        if gps_time == "":
            return "GPS Time field is empty"
        try:
            datetime.time.fromisoformat(gps_time)
        except ValueError:
            return "GPS Time field is not a valid time"
        return None

    @staticmethod
    def _validate_gps_timezone(gps_tz: str) -> Optional[str]:
        if gps_tz < 0:
            return "GPS Timezone field is empty"
        return None

    @staticmethod
    def _validate_output_directory(output_dir: str) -> Optional[str]:
        if output_dir == "":
            return "Export directory is empty"
        path = Path(output_dir.replace("file://", ""))
        if not path.exists():
            return "Export directory does not exist"
        if not path.is_dir():
            return "Export directory is not a directory"
        return None

    @staticmethod
    def _validate_ifdo_enable(ifdo_enable: bool) -> Optional[str]:
        return None

    @staticmethod
    def _validate_image_set_name(ifdo_enable: bool, image_set_name: str) -> Optional[str]:
        if ifdo_enable and image_set_name == "":
            return "Image set name is empty"
        return None

    @staticmethod
    def _validate_image_context(ifdo_enable: bool, image_context: str) -> Optional[str]:
        if ifdo_enable and image_context == "":
            return "Image context is empty"
        return None

    @staticmethod
    def _validate_project_name(ifdo_enable: bool, project_name: str) -> Optional[str]:
        if ifdo_enable and project_name == "":
            return "Project name is empty"
        return None

    @staticmethod
    def _validate_campaign_name(ifdo_enable: bool, campaign_name: str) -> Optional[str]:
        if ifdo_enable and campaign_name == "":
            return "Campaign name is empty"
        return None

    @staticmethod
    def _validate_pi_name(ifdo_enable: bool, pi_name: str) -> Optional[str]:
        if ifdo_enable and pi_name == "":
            return "PI name is empty"
        return None

    @staticmethod
    def _validate_pi_orcid(ifdo_enable: bool, pi_orcid: str) -> Optional[str]:
        if ifdo_enable and pi_orcid != "":
            # ensure that ORCID is correct format
            if not re.match(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$", pi_orcid):
                return "Principal Investigator ORCID is not in the correct format"
        return None

    @staticmethod
    def _validate_collectors_name(ifdo_enable: bool, collectors_name: str) -> Optional[str]:
        if ifdo_enable and collectors_name == "":
            return "Collector's name is empty"
        return None
    
    @staticmethod
    def _validate_collectors_orcid(ifdo_enable: bool, collectors_orcid: str) -> Optional[str]:
        if ifdo_enable and collectors_orcid != "":
            # ensure that ORCID is correct format
            if not re.match(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$", collectors_orcid):
                return "Collector's ORCID is not in the correct format"
        return None

    @staticmethod
    def _validate_organisation(ifdo_enable: bool, organisation: str) -> Optional[str]:
        if ifdo_enable and organisation == "":
            return "Organisation is empty"
        return None

    @staticmethod
    def _validate_license(ifdo_enable: bool, license: str) -> Optional[str]:
        if ifdo_enable and license == "":
            return "License is empty"
        return None

    @staticmethod
    def _validate_distance_above_ground(ifdo_enable: bool, distance: str) -> Optional[str]:
        if ifdo_enable and distance == "":
            return "Distance above ground is empty"
        try:
            float(distance)
        except ValueError:
            return "Distance above ground is not a number"
        return None

    @staticmethod
    def _validate_image_abstract(ifdo_enable: bool, image_abstract: str) -> Optional[str]:
        return None

    @staticmethod
    def _validate_image_objective(ifdo_enable: bool, image_objective: str) -> Optional[str]:
        return None

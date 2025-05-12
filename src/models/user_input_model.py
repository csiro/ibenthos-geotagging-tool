

import datetime
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
    ifdoEnableChanged = pyqtSignal(bool)
    siteLatitudeChanged = pyqtSignal(str)
    siteLongitudeChanged = pyqtSignal(str)
    exportDirectoryChanged = pyqtSignal(str)
    projectNameChanged = pyqtSignal(str)
    campaignNameChanged = pyqtSignal(str)
    siteIDChanged = pyqtSignal(str)
    collectionStartDateChanged = pyqtSignal(str)
    collectionStartTimeChanged = pyqtSignal(str)
    collectionEndDateChanged = pyqtSignal(str)
    collectionEndTimeChanged = pyqtSignal(str)
    cameraIDChanged = pyqtSignal(str)
    distanceAboveGroundChanged = pyqtSignal(str)
    collectorNameChanged = pyqtSignal(str)
    collectorORCIDChanged = pyqtSignal(str)
    organisationChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._import_dir = ""
        self._gpx_filepath = ""
        self._gps_photo_filepath = ""
        self._gps_date = ""
        self._gps_time = ""
        self._gps_timezone_index = 0
        self._site_lat = ""
        self._site_lon = ""
        self._export_dir = ""
        self._ifdo_enable = False
        self._project_name = ""
        self._campaign_name = ""
        self._site_id = ""
        self._col_start_date = ""
        self._col_start_time = ""
        self._col_end_date = ""
        self._col_end_time = ""
        self._camera_id = ""
        self._distance_above_ground = ""
        self._collector_name = ""
        self._collector_orcid = ""
        self._organisation = ""

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

    @pyqtProperty(str, notify=siteLatitudeChanged)
    def siteLatitude(self):
        return self._site_lat

    @siteLatitude.setter
    def siteLatitude(self, lat):
        if self._site_lat != lat:
            self._site_lat = lat
            self.siteLatitudeChanged.emit(lat)

    @pyqtProperty(str, notify=siteLongitudeChanged)
    def siteLongitude(self):
        return self._site_lon

    @siteLongitude.setter
    def siteLongitude(self, lon):
        if self._site_lon != lon:
            self._site_lon = lon
            self.siteLongitudeChanged.emit(lon)

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

    @pyqtProperty(str, notify=siteIDChanged)
    def siteID(self):
        return self._site_id

    @siteID.setter
    def siteID(self, site_id):
        if self._site_id != site_id:
            self._site_id = site_id
            self.siteIDChanged.emit(site_id)

    @pyqtProperty(str, notify=collectionStartDateChanged)
    def collectionStartDate(self):
        return self._col_start_date

    @collectionStartDate.setter
    def collectionStartDate(self, date):
        if self._col_start_date != date:
            self._col_start_date = date
            self.collectionStartDateChanged.emit(date)

    @pyqtProperty(str, notify=collectionStartTimeChanged)
    def collectionStartTime(self):
        return self._col_start_time

    @collectionStartTime.setter
    def collectionStartTime(self, time):
        if self._col_start_time != time:
            self._col_start_time = time
            self.collectionStartTimeChanged.emit(time)

    @pyqtProperty(str, notify=collectionEndDateChanged)
    def collectionEndDate(self):
        return self._col_end_date

    @collectionEndDate.setter
    def collectionEndDate(self, date):
        if self._col_end_date != date:
            self._col_end_date = date
            self.collectionEndDateChanged.emit(date)

    @pyqtProperty(str, notify=collectionEndTimeChanged)
    def collectionEndTime(self):
        return self._col_end_time

    @collectionEndTime.setter
    def collectionEndTime(self, time):
        if self._col_end_time != time:
            self._col_end_time = time
            self.collectionEndTimeChanged.emit(time)

    @pyqtProperty(str, notify=cameraIDChanged)
    def cameraID(self):
        return self._camera_id

    @cameraID.setter
    def cameraID(self, camera_id):
        if self._camera_id != camera_id:
            self._camera_id = camera_id
            self.cameraIDChanged.emit(camera_id)

    @pyqtProperty(str, notify=distanceAboveGroundChanged)
    def distanceAboveGround(self):
        return self._distance_above_ground

    @distanceAboveGround.setter
    def distanceAboveGround(self, distance):
        if self._distance_above_ground != distance:
            self._distance_above_ground = distance
            self.distanceAboveGroundChanged.emit(distance)
    
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

    @pyqtSlot()
    def clearForm(self):
        self.importDirectory = ""
        self.gpxFilepath = ""
        self.gpsPhotoFilepath = ""
        self.gpsDate = ""
        self.gpsTime = ""
        self.gpsTimezoneIndex = 0
        self.siteLatitude = ""
        self.siteLongitude = ""
        self.exportDirectory = ""
        self.projectName = ""
        self.campaignName = ""
        self.siteID = ""
        self.collectionStartDate = ""
        self.collectionStartTime = ""
        self.collectionEndDate = ""
        self.collectionEndTime = ""
        self.cameraID = ""
        self.distanceAboveGround = ""
        self.collectorName = ""
        self.collectorORCID = ""
        self.organisation = ""

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
            self._validate_ifdo_enable : [model.ifdoEnable]
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
        # try:
        #     zoneinfo.ZoneInfo(self.model.gpsTimezoneIndex)
        # except zoneinfo.ZoneInfoNotFoundError:
        #     return "GPS Timezone field is not a valid timezone"
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

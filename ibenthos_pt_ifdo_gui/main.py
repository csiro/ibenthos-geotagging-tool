import os
import sys
import threading
import zoneinfo
from pathlib import Path

import gpxpy
from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine


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

class UserInputModel(QObject):
    importDirectoryChanged = pyqtSignal(str)
    gpxFilepathChanged = pyqtSignal(str)
    gpsPhotoFilepathChanged = pyqtSignal(str)
    gpsDateChanged = pyqtSignal(str)
    gpsTimeChanged = pyqtSignal(str)
    gpsTimezoneIndexChanged = pyqtSignal(int)
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
            print("Import directory changed")

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
        # Check import directory is valid
        path = Path(self.importDirectory)
        print(path)
        if not path.exists() or not path.is_dir():
            return False
        return True

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

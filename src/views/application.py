import logging

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
                               QProgressBar, QVBoxLayout, QWidget)

from .components import (ConfigDateTime, ConfigDirectory, ConfigFileSelector,
                         ConfigMultilineTextBox, ConfigSelector, ConfigTextBox,
                         ControlRow, FeedbackViewer, ImagePreview)

logger = logging.getLogger(__name__)

class MainWindow(QWidget):
    inputDirChanged = Signal(str)
    gpxFileChanged = Signal(str)
    gpsPhotoAvailableChanged = Signal(bool)
    gpsPhotoChanged = Signal(str)
    gpsDateChanged = Signal(str)
    gpsTimeChanged = Signal(str)
    gpsTimezoneIndexChanged = Signal(int)
    cameraTimezoneIndexChanged = Signal(int)
    outputDirChanged = Signal(str)
    ifdoExportChanged = Signal(bool)
    imageSetNameChanged = Signal(str)
    contextChanged = Signal(str)
    projectNameChanged = Signal(str)
    campaignNameChanged = Signal(str)
    piNameChanged = Signal(str)
    piOrcidChanged = Signal(str)
    collectorNameChanged = Signal(str)
    collectorOrcidChanged = Signal(str)
    copyrightOwnerChanged = Signal(str)
    licenseChanged = Signal(str)
    distanceAGChanged = Signal(str)
    imageObjectiveChanged = Signal(str)
    imageAbstractChanged = Signal(str)
    clearFormTriggered = Signal()
    startProcessingTriggered = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("iBenthos Geotagging Tool")
        self.setGeometry(100, 100, 1200, 600)
        self._timezone_index_default = 0

        self._parent_layout = QVBoxLayout()

        # Create a horizontal 3 pane layout
        self._main_layout = QHBoxLayout()

        # Left pane
        self._left_pane = QVBoxLayout()

        # 
        self._input_dir_config = ConfigDirectory(self, label_text="Input photo directory")
        self._input_dir_config.directoryChanged.connect(self.inputDirChanged)
        self._left_pane.addWidget(self._input_dir_config)

        self._gpx_file_config = ConfigFileSelector(self, label_text="GPX file",
                                                   name_filters=["GPX files (*.gpx)"])
        self._gpx_file_config.fileSelected.connect(self.gpxFileChanged)
        self._left_pane.addWidget(self._gpx_file_config)

        self._gps_photo_available_checkbox = QCheckBox("GPS Photo for sync available")
        self._gps_photo_available_checkbox.setChecked(False)
        self._gps_photo_available_checkbox.stateChanged.connect(lambda: self.gpsPhotoAvailableChanged.emit(self._gps_photo_available_checkbox.isChecked()))
        self._gps_photo_available_checkbox.stateChanged.connect(self.enableDisableGPSPhotoFields)
        self._left_pane.addWidget(self._gps_photo_available_checkbox)

        self._gps_photo_config = ConfigFileSelector(self, label_text="GPS Photo")
        self._gps_photo_config.fileSelected.connect(self.gpsPhotoChanged)
        self._left_pane.addWidget(self._gps_photo_config)

        self._image_preview = ImagePreview()
        self._left_pane.addWidget(self._image_preview)
        self._gps_photo_config.fileSelected.connect(self._image_preview.setFilepath)

        self._gps_datetime_config = ConfigDateTime()
        self._gps_datetime_config.label = "Date Time on GPS"
        self._gps_datetime_config.dateChanged.connect(self.gpsDateChanged)
        self._gps_datetime_config.timeChanged.connect(self.gpsTimeChanged)
        self._left_pane.addWidget(self._gps_datetime_config)

        self._gps_timezone_selector = ConfigSelector(options=["Option 1", "Option 2", "Option 3"])
        self._gps_timezone_selector.indexChanged.connect(self.gpsTimezoneIndexChanged)
        self._gps_timezone_selector.currentIndex = self._timezone_index_default
        self._left_pane.addWidget(self._gps_timezone_selector)


        self._camera_timezone_selector = ConfigSelector(options=["Option 1", "Option 2", "Option 3"],
                                                        label="Camera timezone")
        self._camera_timezone_selector.indexChanged.connect(self.cameraTimezoneIndexChanged)
        self._camera_timezone_selector.currentIndex = self._timezone_index_default
        self._left_pane.addWidget(self._camera_timezone_selector)

        # Initially disable GPS photo fields since checkbox is unchecked
        self._gps_photo_config.setEnabled(False)
        self._image_preview.setEnabled(False)
        self._gps_datetime_config.setEnabled(False)
        self._gps_timezone_selector.setEnabled(False)

        self._output_dir_config = ConfigDirectory(self, label_text="Output directory")
        self._output_dir_config.directoryChanged.connect(self.outputDirChanged)
        self._left_pane.addWidget(self._output_dir_config)

        self._ifdo_export_checkbox = QCheckBox("Export as an iFDO dataset")
        self._ifdo_export_checkbox.setChecked(False)
        self._ifdo_export_checkbox.stateChanged.connect(lambda: self.ifdoExportChanged.emit(self._ifdo_export_checkbox.isChecked()))
        self._left_pane.addWidget(self._ifdo_export_checkbox)

        self._main_layout.addLayout(self._left_pane)

        # Middle pane
        self._middle_pane = QVBoxLayout()
        label = QLabel("iFDO details")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._middle_pane.addWidget(label)
        self._image_set_name = ConfigTextBox(self)
        self._image_set_name.label = "Image set name"
        self._image_set_name.defaultValue = "i.e. Site and date identifier"
        self._image_set_name.valueChanged.connect(self.imageSetNameChanged)
        self._middle_pane.addWidget(self._image_set_name)

        self._context = ConfigTextBox(self)
        self._context.label = "Context"
        self._context.defaultValue = "i.e. why is this being collected?"
        self._context.valueChanged.connect(self.contextChanged)
        self._middle_pane.addWidget(self._context)

        self._project_name = ConfigTextBox(self)
        self._project_name.label = "Project name"
        self._project_name.defaultValue = "i.e. iBenthos"
        self._project_name.valueChanged.connect(self.projectNameChanged)
        self._middle_pane.addWidget(self._project_name)

        self._campaign_name = ConfigTextBox(self)
        self._campaign_name.label = "Campaign name"
        self._campaign_name.defaultValue = "i.e. Voyage or trip name"
        self._campaign_name.valueChanged.connect(self.campaignNameChanged)
        self._middle_pane.addWidget(self._campaign_name)

        self._pi_name = ConfigTextBox(self, width_ratio=0.5)
        self._pi_name.label = "Principal Investigator's name"
        self._pi_name.defaultValue = "i.e. Jane Smith"
        self._pi_name.valueChanged.connect(self.piNameChanged)
        self._middle_pane.addWidget(self._pi_name)

        self._pi_orcid = ConfigTextBox(self, width_ratio=0.5)
        self._pi_orcid.label = "PI's ORCID (optional)"
        self._pi_orcid.defaultValue = "0000-0000-0000-0000"
        self._pi_orcid.valueChanged.connect(self.piOrcidChanged)
        self._middle_pane.addWidget(self._pi_orcid)

        self._collector_name = ConfigTextBox(self, width_ratio=0.5)
        self._collector_name.label = "Collector's name"
        self._collector_name.defaultValue = "i.e. Jane Smith"
        self._collector_name.valueChanged.connect(self.collectorNameChanged)
        self._middle_pane.addWidget(self._collector_name)

        self._collector_orcid = ConfigTextBox(self, width_ratio=0.5)
        self._collector_orcid.label = "Collector's ORCID (optional)"
        self._collector_orcid.defaultValue = "0000-0000-0000-0000"
        self._collector_orcid.valueChanged.connect(self.collectorOrcidChanged)
        self._middle_pane.addWidget(self._collector_orcid)

        self._copyright_owner = ConfigTextBox(self, width_ratio=0.5)
        self._copyright_owner.label = "Copyright owner"
        self._copyright_owner.defaultValue = "i.e. University of the Sea"
        self._copyright_owner.valueChanged.connect(self.copyrightOwnerChanged)
        self._middle_pane.addWidget(self._copyright_owner)

        self._license = ConfigTextBox(self, width_ratio=0.5)
        self._license.label = "License"
        self._license.defaultValue = "i.e. CC BY 4.0"
        self._license.value = "CC BY 4.0"
        self._license.valueChanged.connect(self.licenseChanged)
        self._middle_pane.addWidget(self._license)

        self._distance_ag = ConfigTextBox(self, width_ratio=0.7)
        self._distance_ag.label = "Distance above ground (m)"
        self._distance_ag.defaultValue = "i.e. 0.8"
        self._distance_ag.valueChanged.connect(self.distanceAGChanged)
        self._middle_pane.addWidget(self._distance_ag)

        self._image_objective = ConfigTextBox(self)
        self._image_objective.label = "Image objective"
        self._image_objective.defaultValue = "What is the survey goal?"
        self._image_objective.valueChanged.connect(self.imageObjectiveChanged)
        self._middle_pane.addWidget(self._image_objective)

        self._image_abstract = ConfigMultilineTextBox(self)
        self._image_abstract.label = "Image abstract"
        self._image_abstract.defaultValue = "Description of the image set"
        self._image_abstract.valueChanged.connect(self.imageAbstractChanged)
        self._middle_pane.addWidget(self._image_abstract)

        self._middle_widget = QWidget()
        self._middle_widget.setLayout(self._middle_pane)
        self._middle_widget.setFixedWidth(400)
        self._middle_widget.setMinimumWidth(400)

        self._main_layout.addWidget(self._middle_widget)
        self._middle_widget.hide()

        # Right pane
        self._right_pane = QVBoxLayout()
        self._control_row = ControlRow()
        self._right_pane.addWidget(self._control_row)
        self._control_row.startTriggered.connect(self.startProcessingTriggered)
        self._control_row.clearTriggered.connect(self.clearFormTriggered)

        self._feedback_viewer = FeedbackViewer(self)
        self._right_pane.addWidget(self._feedback_viewer)

        self._main_layout.addLayout(self._right_pane)

        # Progress bar
        self._progress_bar = QProgressBar(self)
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setFixedHeight(20)
        self._progress_bar.setAlignment(Qt.AlignCenter)

        self._parent_layout.addLayout(self._main_layout)
        self._parent_layout.addWidget(self._progress_bar)

        # Set the layout for the main window
        self.setLayout(self._parent_layout)

    @Slot(bool)
    def showIFDODetails(self, show: bool):
        if show:
            self._middle_widget.show()
        else:
            self._middle_widget.hide()

    @Slot()
    def enableDisableGPSPhotoFields(self):
        enabled = self._gps_photo_available_checkbox.isChecked()
        self._gps_photo_config.setEnabled(enabled)
        self._image_preview.setEnabled(enabled)
        self._gps_datetime_config.setEnabled(enabled)
        self._gps_timezone_selector.setEnabled(enabled)
        if not enabled:
            # Clear the GPS photo fields if disabled
            self._gps_photo_config.value = ""
            self._image_preview.setFilepath("")
            self._gps_datetime_config.date = ""
            self._gps_datetime_config.time = ""
            self._gps_timezone_selector.currentIndex = self._timezone_index_default

    @Slot(str)
    def setDefaultPath(self, default_path: str):
        self._gps_photo_config.defaultPath = default_path
        self._gpx_file_config.defaultPath = default_path

    @Slot(str)
    def setFeedbackText(self, text: str):
        self._feedback_viewer.setText(text)

    @Slot(int)
    def setProgress(self, current_progress: int):
        if not 0 <= current_progress <= 100:
            logger.warning("Progress received not within bounds! %i", current_progress)
            current_progress = max(0, min(100, current_progress))
        self._progress_bar.setValue(current_progress)

    def setTimezoneOptions(self, options: list):
        self._gps_timezone_selector.setOptions(options)
        self._camera_timezone_selector.setOptions(options)

    @Slot()
    def clearForm(self):
        self._input_dir_config.value = ""
        self._gpx_file_config.value = ""
        self._gps_photo_available_checkbox.setChecked(False)
        self._gps_photo_config.value = ""
        self._gps_datetime_config.date = ""
        self._gps_datetime_config.time = ""
        self._gps_timezone_selector.currentIndex = self._timezone_index_default
        self._camera_timezone_selector.currentIndex = self._timezone_index_default
        self._output_dir_config.value = ""
        self._ifdo_export_checkbox.setChecked(False)

        self._image_set_name.value = ""
        self._context.value = ""
        self._project_name.value = ""
        self._campaign_name.value = ""
        self._pi_name.value = ""
        self._pi_orcid.value = ""
        self._collector_name.value = ""
        self._collector_orcid.value = ""
        self._copyright_owner.value = ""
        self._license.value = "CC BY 4.0"
        self._distance_ag.value = ""
        self._image_objective.value = ""
        self._image_abstract.value = ""
    
    def setTimezoneIndexDefault(self, index: int, reset: bool = False):
        self._timezone_index_default = index
        if reset:
            self._gps_timezone_selector.currentIndex = index
            self._camera_timezone_selector.currentIndex = index
    
    def manuallyTriggerFieldSignals(self):
        self._gps_datetime_config.dateChanged.emit(self._gps_datetime_config.date)
        self._gps_datetime_config.timeChanged.emit(self._gps_datetime_config.time)
        self._image_set_name.valueChanged.emit(self._image_set_name.value)
        self._context.valueChanged.emit(self._context.value)
        self._project_name.valueChanged.emit(self._project_name.value)
        self._campaign_name.valueChanged.emit(self._campaign_name.value)
        self._pi_name.valueChanged.emit(self._pi_name.value)
        self._pi_orcid.valueChanged.emit(self._pi_orcid.value)
        self._collector_name.valueChanged.emit(self._collector_name.value)
        self._collector_orcid.valueChanged.emit(self._collector_orcid.value)
        self._copyright_owner.valueChanged.emit(self._copyright_owner.value)
        self._license.valueChanged.emit(self._license.value)
        self._distance_ag.valueChanged.emit(self._distance_ag.value)
        self._image_objective.valueChanged.emit(self._image_objective.value)
        self._image_abstract.valueChanged.emit(self._image_abstract.value)



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
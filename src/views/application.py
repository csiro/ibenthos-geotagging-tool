"""
application.py: Main window for the iBenthos Geotagging Tool application.
This module provides the main GUI for the application

Copyright (c) 2025
Commonwealth Scientific and Industrial Research Organisation (CSIRO)
ABN 41 687 119 230

Author: Brendan Do <brendan.do@csiro.au>
"""
import logging
import webbrowser

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout,
                               QMainWindow, QProgressBar, QVBoxLayout, QWidget)

from .components import (AboutDialog, ConfigDateTime, ConfigDirectory,
                         ConfigFileSelector, ConfigMultilineTextBox,
                         ConfigSelector, ConfigTextBox, ControlRow,
                         FeedbackViewer, ImagePreview)

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """
    Main application window for the iBenthos Geotagging Tool.
    """
    # pylint: disable=invalid-name
    # Camel case to comply with pyside6 naming conventions

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
    kmlExportChanged = Signal(bool)
    imageSetNameChanged = Signal(str)
    contextChanged = Signal(str)
    projectNameChanged = Signal(str)
    eventNameChanged = Signal(str)
    piNameChanged = Signal(str)
    piOrcidChanged = Signal(str)
    collectorNameChanged = Signal(str)
    collectorOrcidChanged = Signal(str)
    copyrightOwnerChanged = Signal(str)
    licenseChanged = Signal(str)
    distanceAGChanged = Signal(str)
    imageAbstractChanged = Signal(str)
    clearFormTriggered = Signal()
    startProcessingTriggered = Signal()
    aboutTriggered = Signal()
    documentationTriggered = Signal()
    attributionExportChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("iBenthos Geotagging Tool")
        self.setGeometry(100, 100, 1300, 600)
        self._timezone_index_default = 0

        self._generate_window_layout()

        # UI Config defaults
        # Initially disable GPS photo fields since checkbox is unchecked
        self._gps_photo_config.setEnabled(False)
        self._image_preview.setEnabled(False)
        self._gps_datetime_config.setEnabled(False)
        self._gps_timezone_selector.setEnabled(False)

        # Initially disable attribution fields since checkbox is unchecked
        self._attribution_group = [self._pi_name, self._pi_orcid,
                                   self._collector_name, self._collector_orcid,
                                   self._copyright_owner, self._license,
                                   self._ifdo_export_checkbox]

        for widget in self._attribution_group:
            widget.setEnabled(False)

        # Disable iFDO export fields initially
        self._ifdo_group = [self._image_set_name, self._context,
                            self._project_name, self._event_name,
                            self._distance_ag, self._image_abstract]

        for widget in self._ifdo_group:
            widget.setEnabled(False)

    def _generate_window_layout(self):
        """
        Generate the main window layout with all components.
        """
        # Create menubar
        self._create_menubar()

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self._parent_layout = QVBoxLayout(central_widget)

        # Create a horizontal 3 pane layout
        self._main_layout = QHBoxLayout()

        # Left pane
        self._left_pane = QVBoxLayout()

        self._input_dir_config = ConfigDirectory(self, label_text="Input photo directory")
        self._input_dir_config.directoryChanged.connect(self.inputDirChanged)
        self._input_dir_config.setToolTip("Select a directory with photos to geotag.")
        self._left_pane.addWidget(self._input_dir_config)

        self._gpx_file_config = ConfigFileSelector(self, label_text="GPX file",
                                                   name_filters=["GPX files (*.gpx)"])
        self._gpx_file_config.fileSelected.connect(self.gpxFileChanged)
        self._gpx_file_config.setToolTip("Select a GPX file containing the GPS track data for "
                                         "geotagging your photos.")
        self._left_pane.addWidget(self._gpx_file_config)

        self._camera_timezone_selector = ConfigSelector(options=["Option 1", "Option 2",
                                                                 "Option 3"],
                                                        label="Camera timezone")
        self._camera_timezone_selector.indexChanged.connect(self.cameraTimezoneIndexChanged)
        self._camera_timezone_selector.currentIndex = self._timezone_index_default
        self._camera_timezone_selector.setToolTip("Select the timezone your camera was set to when"
                                                  " taking the photos.")
        self._left_pane.addWidget(self._camera_timezone_selector)

        self._output_dir_config = ConfigDirectory(self, label_text="Output directory")
        self._output_dir_config.directoryChanged.connect(self.outputDirChanged)
        self._output_dir_config.setToolTip("Choose where to save the geotagged photos.")
        self._left_pane.addWidget(self._output_dir_config)

        self._gps_photo_available_checkbox = QCheckBox("GPS Photo for sync available")
        self._gps_photo_available_checkbox.setChecked(False)
        self._gps_photo_available_checkbox.stateChanged.connect(
            lambda: self.gpsPhotoAvailableChanged.emit(
                self._gps_photo_available_checkbox.isChecked()))
        self._gps_photo_available_checkbox.stateChanged.connect(self.enableDisableGPSPhotoFields)
        self._gps_photo_available_checkbox.setToolTip("Check this if you have taken a photo for the"
                                                      " GPS unit with the date & time. This "
                                                      "improves accuracy when camera and GPS clocks"
                                                      " aren't perfectly synchronized.")
        self._left_pane.addWidget(self._gps_photo_available_checkbox)

        self._gps_photo_config = ConfigFileSelector(self, label_text="GPS Photo")
        self._gps_photo_config.fileSelected.connect(self.gpsPhotoChanged)
        self._gps_photo_config.setToolTip("Select photo taken with the GPS unit date & time. This "
                                          "photo will be used to synchronize the camera time with"
                                          " GPS time.")
        self._left_pane.addWidget(self._gps_photo_config)

        self._image_preview = ImagePreview()
        self._left_pane.addWidget(self._image_preview)
        self._gps_photo_config.fileSelected.connect(self._image_preview.setFilepath)

        self._gps_datetime_config = ConfigDateTime()
        self._gps_datetime_config.label = "Date Time on GPS"
        self._gps_datetime_config.dateChanged.connect(self.gpsDateChanged)
        self._gps_datetime_config.timeChanged.connect(self.gpsTimeChanged)
        self._gps_datetime_config.setToolTip("Enter the exact date and time on your GPS unit.")
        self._left_pane.addWidget(self._gps_datetime_config)

        self._gps_timezone_selector = ConfigSelector(options=["Option 1", "Option 2", "Option 3"])
        self._gps_timezone_selector.indexChanged.connect(self.gpsTimezoneIndexChanged)
        self._gps_timezone_selector.currentIndex = self._timezone_index_default
        self._gps_timezone_selector.setToolTip("Select the timezone your GPS device was set to when"
                                               " recording the reference photo location.")
        self._left_pane.addWidget(self._gps_timezone_selector)

        self._main_layout.addLayout(self._left_pane)

        # Middle pane
        self._middle_pane = QVBoxLayout()

        self._kml_export = QCheckBox("Export a KMZ preview file")
        self._kml_export.setChecked(False)
        self._kml_export.stateChanged.connect(
            lambda: self.kmlExportChanged.emit(self._kml_export.isChecked()))
        self._kml_export.setToolTip("Selecting this will generate a KMZ file, which contains the "
                                    "locations of each photo and a circular thumbnail of each "
                                    "photo. If this KMZ is distributed with the rest of the output "
                                    "directory, it will also provide a preview of the images. "
                                    "This file can be opened in software such as Google Earth and "
                                    "GIS applications. ")
        self._middle_pane.addWidget(self._kml_export)

        self._attribution_export = QCheckBox("Add attribution metadata")
        self._attribution_export.setChecked(False)
        self._attribution_export.stateChanged.connect(
            lambda: self.attributionExportChanged.emit(self._attribution_export.isChecked()))
        self._attribution_export.setToolTip("Check this to embed researcher and copyright "
                                            "information directly into the photo metadata.")
        self._middle_pane.addWidget(self._attribution_export)

        self._pi_name = ConfigTextBox(self, width_ratio=0.5,
                                      label="Principal Investigator's name",
                                      default_value="Jane Smith",
                                      value_changed_signal_connect=self.piNameChanged,
                                      tooltip="Enter the name of the principal investigator "
                                              "responsible for this research project.")
        self._middle_pane.addWidget(self._pi_name)

        self._pi_orcid = ConfigTextBox(self, width_ratio=0.5,
                                       label="PI's ORCID (optional)",
                                       default_value="0000-0000-0000-0000",
                                       value_changed_signal_connect=self.piOrcidChanged,
                                       tooltip="Enter the Principal Investigator's ORCID. "
                                               "Format: 0000-0000-0000-0000")
        self._middle_pane.addWidget(self._pi_orcid)

        self._collector_name = ConfigTextBox(self, width_ratio=0.5,
                                             label="Collector's name",
                                             default_value="Jane Smith",
                                             value_changed_signal_connect=self.collectorNameChanged,
                                             tooltip="Enter the name of the person who "
                                                     "collected/took these photos.")
        self._middle_pane.addWidget(self._collector_name)

        self._collector_orcid = ConfigTextBox(self, width_ratio=0.5,
                                              label="Collector's ORCID (optional)",
                                              default_value="0000-0000-0000-0000",
                                              value_changed_signal_connect=\
                                                self.collectorOrcidChanged,
                                              tooltip="Enter the image collector's ORCID. "
                                                      "Format: 0000-0000-0000-0000")
        self._middle_pane.addWidget(self._collector_orcid)

        self._copyright_owner = ConfigTextBox(self, width_ratio=0.5,
                                              label="Copyright statement",
                                              default_value=\
                                                "(c) 2025 University of the Sea",
                                              value_changed_signal_connect=\
                                                self.copyrightOwnerChanged,
                                              tooltip="Enter your copyright statement.")
        self._middle_pane.addWidget(self._copyright_owner)


        self._license = ConfigTextBox(self, width_ratio=0.5, label="License",
                                      default_value="CC BY 4.0",
                                      value_changed_signal_connect=self.licenseChanged,
                                      tooltip="Specify the license under which these images are "
                                              "made available (e.g., CC BY 4.0, All Rights "
                                              "Reserved).")
        self._middle_pane.addWidget(self._license)

        self._ifdo_export_checkbox = QCheckBox("Export an iFDO file")
        self._ifdo_export_checkbox.setChecked(False)
        self._ifdo_export_checkbox.stateChanged.connect(lambda:
                                self.ifdoExportChanged.emit(self._ifdo_export_checkbox.isChecked()))
        self._ifdo_export_checkbox.setToolTip("Create an iFDO (image FAIR Digital Object)"
                                              " metadata file containing detailed information about"
                                              " the image collection for marine research purposes.")
        self._middle_pane.addWidget(self._ifdo_export_checkbox)

        self._image_set_name = ConfigTextBox(self, label="Image set name",
                                             default_value="Seagrass Survey: Site A, 2025-06",
                                             value_changed_signal_connect=self.imageSetNameChanged,
                                             tooltip="Enter a name for the image set.")
        self._middle_pane.addWidget(self._image_set_name)

        self._context = ConfigTextBox(self, label="Context",
                                      default_value="Higher-level \"umbrella\" project",
                                      value_changed_signal_connect=self.contextChanged,
                                      tooltip="Name of the higher-level project or context this "
                                              "data is being collected for.")
        self._middle_pane.addWidget(self._context)

        self._project_name = ConfigTextBox(self, label="Project name",
                                           default_value="Seagrass expedition June 25",
                                           value_changed_signal_connect=self.projectNameChanged,
                                           tooltip="Enter the lower-level project, expedition, "
                                                   "cruise or experiment.")
        self._middle_pane.addWidget(self._project_name)

        self._event_name = ConfigTextBox(self, label="Event name",
                                         default_value="Site A, 2025-06",
                                         value_changed_signal_connect=self.eventNameChanged,
                                         tooltip="Specify the event for the project, such as the "
                                                 "site name etc.")
        self._middle_pane.addWidget(self._event_name)

        self._distance_ag = ConfigTextBox(self, width_ratio=0.7,
                                          label="Distance above ground (m)",
                                          default_value=" 0.8",
                                          value_changed_signal_connect=self.distanceAGChanged,
                                          tooltip="Enter the typical distance in meters between "
                                                  "the camera and the seafloor/ground when these "
                                                  "images were taken.")
        self._middle_pane.addWidget(self._distance_ag)

        self._image_abstract = ConfigMultilineTextBox(self)
        self._image_abstract.label = "Abstract"
        self._image_abstract.defaultValue = "Description of the image set"
        self._image_abstract.valueChanged.connect(self.imageAbstractChanged)
        self._image_abstract.setToolTip("Provide a description on what, when, where, why"
                                        " and how the data was collected.")
        self._middle_pane.addWidget(self._image_abstract)

        self._main_layout.addLayout(self._middle_pane)

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

    def _create_menubar(self):
        """Create the application menubar with Help menu."""
        menubar = self.menuBar()

        # Create Help menu
        help_menu = menubar.addMenu("&Help")

        # About action
        about_action = QAction("&About", self)
        about_action.setStatusTip("Show information about the application")
        about_action.triggered.connect(self.aboutTriggered.emit)
        help_menu.addAction(about_action)

        # Documentation action
        documentation_action = QAction("&Documentation", self)
        documentation_action.setStatusTip("Open application documentation")
        documentation_action.triggered.connect(self.documentationTriggered.emit)
        help_menu.addAction(documentation_action)

    @Slot()
    def enableDisableAttributionFields(self):
        """
        This method enables or disables the attribution fields based on the state of the
        attribution export checkbox.
        If the checkbox is unchecked, all attribution fields are cleared and disabled.
        If the checkbox is checked, all attribution fields are enabled.
        """
        enabled = self._attribution_export.isChecked()
        for widget in self._attribution_group:
            widget.setEnabled(enabled)
            if not enabled and isinstance(widget, ConfigTextBox):
                widget.value = ""
        if not enabled:
            self._ifdo_export_checkbox.setChecked(False)
            self._license.value = "CC BY 4.0"  # Reset license to default

    @Slot()
    def enableDisableIFDODetails(self):
        """
        This method enables or disables the iFDO export fields based on the state of the
        iFDO export checkbox.
        If the checkbox is unchecked, all iFDO fields are cleared and disabled.
        If the checkbox is checked, all iFDO fields are enabled.
        """
        enabled =self._ifdo_export_checkbox.isChecked()
        for widget in self._ifdo_group:
            widget.setEnabled(enabled)
            if not enabled:
                widget.value = ""  # Clear the field if disabled

    @Slot()
    def enableDisableGPSPhotoFields(self):
        """
        This method enables or disables the GPS photo fields based on the state of the
        GPS photo available checkbox.
        If the checkbox is unchecked, all GPS photo fields are cleared and disabled.
        If the checkbox is checked, all GPS photo fields are enabled.
        """
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
        """
        This method sets the default path for the GPS Photo selector and GPX file selector.
        Args:
            default_path (str): The default path to set for the GPS Photo and GPX file selectors.
        """
        self._gps_photo_config.defaultPath = default_path
        self._gpx_file_config.defaultPath = default_path

    @Slot(str)
    def setFeedbackText(self, text: str):
        """
        This method sets the feedback text in the feedback viewer.
        Args:
            text (str): The text to display in the feedback viewer.
        """
        self._feedback_viewer.setText(text)

    @Slot(int)
    def setProgress(self, current_progress: int):
        """
        This method sets the progress value of the progress bar.
        Args:
            current_progress (int): The current progress value to set in the progress bar. [0-100]
        """
        if not 0 <= current_progress <= 100:
            logger.warning("Progress received not within bounds! %i", current_progress)
            current_progress = max(0, min(100, current_progress))
        self._progress_bar.setValue(current_progress)

    def setTimezoneOptions(self, options: list):
        """
        This method sets the options for the GPS and camera timezone selectors.
        Args:
            options (list): A list of timezone options to set for both selectors."""
        self._gps_timezone_selector.setOptions(options)
        self._camera_timezone_selector.setOptions(options)

    @Slot()
    def clearForm(self):
        """
        This method clears all user input fields in the main window.
        """
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
        self._event_name.value = ""
        self._pi_name.value = ""
        self._pi_orcid.value = ""
        self._collector_name.value = ""
        self._collector_orcid.value = ""
        self._copyright_owner.value = ""
        self._license.value = "CC BY 4.0"
        self._distance_ag.value = ""
        self._image_abstract.value = ""
        self._attribution_export.setChecked(False)
        self._kml_export.setChecked(False)

    def setTimezoneIndexDefault(self, index: int, reset: bool = False):
        """
        This method sets the default timezone index for both GPS and camera timezone selectors.
        Args:
            index (int): The index to set as the default timezone index.
            reset (bool): If True, resets the current index of both selectors to the default index.
        """
        self._timezone_index_default = index
        if reset:
            self._gps_timezone_selector.currentIndex = index
            self._camera_timezone_selector.currentIndex = index

    def manuallyTriggerFieldSignals(self):
        """
        This method manually triggers the valueChanged signals for all text fields.
        This is useful when you want to ensure that all fields emit their changed signals
        even if the values haven't changed.
        """
        self._gps_datetime_config.dateChanged.emit(self._gps_datetime_config.date)
        self._gps_datetime_config.timeChanged.emit(self._gps_datetime_config.time)
        self._image_set_name.valueChanged.emit(self._image_set_name.value)
        self._context.valueChanged.emit(self._context.value)
        self._project_name.valueChanged.emit(self._project_name.value)
        self._event_name.valueChanged.emit(self._event_name.value)
        self._pi_name.valueChanged.emit(self._pi_name.value)
        self._pi_orcid.valueChanged.emit(self._pi_orcid.value)
        self._collector_name.valueChanged.emit(self._collector_name.value)
        self._collector_orcid.valueChanged.emit(self._collector_orcid.value)
        self._copyright_owner.valueChanged.emit(self._copyright_owner.value)
        self._license.valueChanged.emit(self._license.value)
        self._distance_ag.valueChanged.emit(self._distance_ag.value)
        self._image_abstract.valueChanged.emit(self._image_abstract.value)

    def showAboutDialog(self, version="Unknown", build_hash="Unknown"):
        """
        This method displays the About dialog.
        """
        about_dialog = AboutDialog(self, version=version, build_hash=build_hash)
        about_dialog.exec()

    def OpenDocumentationURL(self, url="https://github.com/csiro/ibenthos-geotagging-tool"):
        """
        This method opens documentation URL in default browser.
        Args:
            url (str): The URL to open in the default web browser.
                       Defaults to the GitHub repository of the project.
        """
        webbrowser.open(url)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

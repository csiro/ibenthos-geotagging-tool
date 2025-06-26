import os

from PySide6.QtCore import QRegularExpression, QSize, Qt, Signal, Slot
from PySide6.QtGui import QPixmap, QRegularExpressionValidator, QTextOption
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialog, QDialogButtonBox,
                               QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QScrollArea, QSizePolicy,
                               QTextEdit, QVBoxLayout, QWidget)


class ConfigDateTime(QWidget):
    dateChanged = Signal(str)
    timeChanged = Signal(str)

    def __init__(self, width_ratio=0.3):
        super().__init__()
        self.width_ratio = width_ratio

        # Layout setup
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        self.setMinimumWidth(300)

        # Label (equivalent to QML Text with id=configName)
        self.configName = QLabel("Label", self)
        layout.addWidget(self.configName, int(self.width_ratio * 100))

        # Date Field (QLineEdit with validator)
        self.configDate = QLineEdit(self)
        self.configDate.setPlaceholderText("YYYY-MM-DD")
        date_regex = QRegularExpression(
            r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
        )
        date_validator = QRegularExpressionValidator(date_regex, self.configDate)
        self.configDate.setValidator(date_validator)
        self.configDate.editingFinished.connect(lambda: self.dateChanged.emit(self.date))
        layout.addWidget(self.configDate, int((1 - self.width_ratio) / 2 * 100))

        # Time Field (QLineEdit with validator)
        self.configTime = QLineEdit(self)
        self.configTime.setPlaceholderText("HH:MM:SS")
        time_regex = QRegularExpression(
            r"^(0?[0-9]|1[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])$"
        )
        time_validator = QRegularExpressionValidator(time_regex, self.configTime)
        self.configTime.setValidator(time_validator)
        self.configTime.editingFinished.connect(lambda: self.timeChanged.emit(self.time))
        layout.addWidget(self.configTime, int((1 - self.width_ratio) / 2 * 100))

        self.setLayout(layout)

    @property
    def label(self):
        return self.configName.text()

    @label.setter
    def label(self, value):
        self.configName.setText(value)

    @property
    def date(self):
        return self.configDate.text()

    @date.setter
    def date(self, value):
        self.configDate.setText(value)
        self.configDate.editingFinished.emit()

    @property
    def time(self):
        return self.configTime.text()

    @time.setter
    def time(self, value):
        self.configTime.setText(value)
        self.configTime.editingFinished.emit()

class ConfigMultilineTextBox(QWidget):
    valueChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumHeight(200)
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Label (configName)
        self.configName = QLabel("Label", self)
        self.configName.setMinimumHeight(25)
        self.configName.setMaximumHeight(50)
        layout.addWidget(self.configName)

        # Text Area inside Scroll Area (configValue)
        self.configValue = QTextEdit(self)
        self.configValue.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.configValue.setPlaceholderText("Default")
        self.configValue.setMinimumHeight(75)
        self.configValue.setMaximumHeight(150)
        self.configValue.textChanged.connect(lambda: self.valueChanged.emit(self.value))

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setWidget(self.configValue)
        scroll_area.setMinimumHeight(75)
        scroll_area.setMaximumHeight(150)

        layout.addWidget(scroll_area)

        self.setLayout(layout)

    @property
    def label(self):
        return self.configName.text()

    @label.setter
    def label(self, value):
        self.configName.setText(value)

    @property
    def defaultValue(self):
        return self.configValue.placeholderText()

    @defaultValue.setter
    def defaultValue(self, value):
        self.configValue.setPlaceholderText(value)

    @property
    def value(self):
        return self.configValue.toPlainText()

    @value.setter
    def value(self, val):
        self.configValue.setPlainText(val)
        self.configValue.textChanged.emit()

class ConfigTextBox(QWidget):
    valueChanged = Signal(str)

    def __init__(self, parent=None, width_ratio=0.3, label="Label", default_value="Default",
                 value_changed_signal_connect=None, tooltip=None):
        super().__init__(parent)
        self.width_ratio = width_ratio
        self.setMinimumWidth(300)

        self.setMinimumHeight(25)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Label (configName)
        self.configName = QLabel("Label", self)
        layout.addWidget(self.configName, int(self.width_ratio * 100))

        # Text Field (configValue)
        self.configValue = QLineEdit(self)
        self.configValue.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.configValue.editingFinished.connect(lambda : self.valueChanged.emit(self.value))
        layout.addWidget(self.configValue, int((1 - self.width_ratio) * 100))

        self.setLayout(layout)

        # Set initial values
        self.label = label
        self.defaultValue = default_value
        if value_changed_signal_connect:
            self.valueChanged.connect(value_changed_signal_connect)

        if tooltip:
            self.setToolTip(tooltip)

    @property
    def label(self):
        return self.configName.text()

    @label.setter
    def label(self, value):
        self.configName.setText(value)

    @property
    def defaultValue(self):
        return self.configValue.placeholderText()

    @defaultValue.setter
    def defaultValue(self, value):
        self.configValue.setPlaceholderText(value)

    @property
    def value(self):
        return self.configValue.text()

    @value.setter
    def value(self, val):
        self.configValue.setText(val)
        self.configValue.editingFinished.emit()

class ConfigDirectory(QWidget):
    directoryChanged = Signal(str)  # emits the selected directory

    def __init__(self, parent=None, label_text="Input directory", default_path="", width_ratio=0.3):
        super().__init__(parent)
        self.width_ratio = width_ratio
        self.setMinimumWidth(300)

        self.importDirectory = default_path

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Label
        self.inputTextField = QLabel(label_text + ": ", self)
        layout.addWidget(self.inputTextField, int(self.width_ratio * 100))

        # Read-only TextField for selected path
        self.importDirPathField = QLineEdit(self)
        self.importDirPathField.setPlaceholderText(f"Select the {label_text}...")
        self.importDirPathField.setReadOnly(True)
        self.importDirPathField.setText(default_path)
        self.importDirPathField.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.importDirPathField, int((1 - self.width_ratio - 0.1) * 100))

        # Browse Button
        self.browseButton = QPushButton("Browse", self)
        self.browseButton.clicked.connect(self.openFolderDialog)
        layout.addWidget(self.browseButton, 10)

        self.setLayout(layout)

    def openFolderDialog(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select a directory", self.importDirectory or ""
        )
        if dir_path:
            self.importDirectory = dir_path
            self.importDirPathField.setText(dir_path)
            self.directoryChanged.emit(dir_path)

    @property
    def value(self):
        return self.importDirectory

    @value.setter
    def value(self, path):
        self.importDirectory = path
        self.importDirPathField.setText(path)
        self.directoryChanged.emit(path)

class ConfigFileSelector(QWidget):
    fileSelected = Signal(str)  # Emits when a file is selected

    def __init__(self, parent=None, label_text="GPS photo", name_filters=None, default_path="",
                 width_ratio=0.3):
        super().__init__(parent)
        self._label_text = label_text
        self.width_ratio = width_ratio
        self.setMinimumWidth(300)
        self.defaultPath = default_path

        self.selectedFile = default_path
        self.name_filters = name_filters or ["Image files (*.jpg *.jpeg *.png *.bmp)"]

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Label
        self.gpsPhotoTextField = QLabel(self._label_text + ": ", self)
        layout.addWidget(self.gpsPhotoTextField, int(self.width_ratio * 100))

        # Read-only file path field
        self.gpsPhotoPathField = QLineEdit(self)
        self.gpsPhotoPathField.setPlaceholderText(f"Select the {self._label_text}...")
        self.gpsPhotoPathField.setReadOnly(True)
        self.gpsPhotoPathField.setText(default_path)
        self.gpsPhotoPathField.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.gpsPhotoPathField, int((1 - self.width_ratio - 0.1) * 100))

        # Browse button
        self.browseButton = QPushButton("Browse", self)
        self.browseButton.clicked.connect(self.openFileDialog)
        layout.addWidget(self.browseButton, 10)

        self.setLayout(layout)

    def openFileDialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Select the {self._label_text}",
            self.defaultPath,
            ";;".join(self.name_filters)
        )
        if file_path:
            self.selectedFile = file_path
            self.gpsPhotoPathField.setText(file_path)
            self.fileSelected.emit(file_path)

    @property
    def value(self):
        return self.selectedFile

    @value.setter
    def value(self, path):
        self.selectedFile = path
        self.gpsPhotoPathField.setText(path)
        self.fileSelected.emit(path)

class ImagePreview(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(QSize(300, 300))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setScaledContents(False)  # Prevents stretching, we'll scale manually

        self._filepath = None

    @Slot(str)
    def setFilepath(self, path):
        if not os.path.isfile(path):
            self.clear()
            self.setText("Image not found")
            return

        self._filepath = path
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            self.setPixmap(scaled)
        else:
            self.setText("Invalid image")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Re-scale image when resized
        if self._filepath and os.path.isfile(self._filepath):
            self.setFilepath(self._filepath)

class ConfigSelector(QWidget):
    indexChanged = Signal(int)  # emits when the selected index changes

    def __init__(self, parent=None, options=None, label="GPS timezone", default_index=0):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.label = QLabel(label + ": ", self)
        layout.addWidget(self.label)

        self.comboBox = QComboBox(self)
        layout.addWidget(self.comboBox)

        if options:
            self.setOptions(options)

        self.comboBox.setCurrentIndex(default_index)
        self.comboBox.currentIndexChanged.connect(self.indexChanged)

        self.setLayout(layout)

    def _on_index_changed(self, index):
        self.indexChanged.emit(index)

    def setOptions(self, options):
        self.comboBox.clear()
        self.comboBox.addItems(options)

    @property
    def currentIndex(self):
        return self.comboBox.currentIndex()

    @currentIndex.setter
    def currentIndex(self, index):
        self.comboBox.setCurrentIndex(index)


class FeedbackViewer(QWidget):
    def __init__(self, parent=None, default_text="Feedback messages will be displayed here..."):
        super().__init__(parent)

        # Layout for the container widget
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Text area inside scroll view
        self.textArea = QTextEdit()
        self.textArea.setPlaceholderText(default_text)
        self.textArea.setReadOnly(True)
        self.textArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # ScrollArea wrapper
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.textArea)
        self.scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.scrollArea)

        self.setLayout(layout)

    def setText(self, text: str):
        self.textArea.setPlainText(text)

    def appendText(self, text: str):
        self.textArea.append(text)

    def clear(self):
        self.textArea.clear()

    def setPlaceholderText(self, text: str):
        self.textArea.setPlaceholderText(text)

    @property
    def text(self):
        return self.textArea.toPlainText()

class ControlRow(QWidget):
    clearTriggered = Signal()
    startTriggered = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        self.clearButton = QPushButton("Clear Form")
        self.clearButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.clearButton.clicked.connect(self.clearTriggered)
        layout.addWidget(self.clearButton, alignment=Qt.AlignHCenter)

        self.startButton = QPushButton("Start processing")
        self.startButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.startButton.clicked.connect(self.startTriggered)
        layout.addWidget(self.startButton, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

class AboutDialog(QDialog):
    """About dialog for the application."""

    def __init__(self, parent=None, version="Unknown", build_hash="Unknown"):
        super().__init__(parent)
        self.setWindowTitle("About iBenthos Geotagging Tool")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout(self)

        # Application name and version
        title_label = QLabel("iBenthos Geotagging Tool")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)

        version_label = QLabel(f"Version: {version}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        build_label = QLabel(f"Build: {build_hash}")
        build_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(build_label)

        # Description
        description = QLabel(
            "A PySide6 desktop application that helps researchers geotag underwater photos "
            "using GPS data from transect files. The application allows users to synchronize "
            "underwater images with GPS tracks and optionally export metadata in iFDO format "
            "for marine research."
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("margin: 20px;")
        layout.addWidget(description)

        # Copyright and license
        copyright_label = QLabel("© 2025 CSIRO")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)

        # OK button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QVBoxLayout

    app = QApplication([])

    main_window = QWidget()
    layout = QVBoxLayout(main_window)

    widget = ConfigDateTime()
    widget.label = "Start Time"
    widget.date = "2025-05-19"
    widget.time = "15:30:00"

    layout.addWidget(widget)


    widget = ConfigMultilineTextBox()
    widget.label = "Description"
    widget.defaultValue = "Enter detailed config here..."
    widget.value = "Initial value"

    layout.addWidget(widget)


    widget = ConfigTextBox()
    widget.label = "Username"
    widget.defaultValue = "Enter username"
    widget.value = "admin"

    layout.addWidget(widget)


    widget = ConfigDirectory(label_text="Input photo directory")
    widget.directoryChanged.connect(lambda path: print(f"Selected directory: {path}"))

    layout.addWidget(widget)

    widget = ConfigFileSelector(label_text="GPX file")
    widget.fileSelected.connect(lambda path: print(f"Selected file: {path}"))

    layout.addWidget(widget)


    image_preview = ImagePreview()
    layout.addWidget(image_preview)

    img_browse = ConfigFileSelector(label_text="GPS Photo")
    img_browse.fileSelected.connect(image_preview.setFilepath)
    layout.addWidget(img_browse)

    widget = ConfigSelector(options=["Option 1", "Option 2", "Option 3"], label="Select Option")
    widget.indexChanged.connect(lambda index: print(f"Selected index: {index}"))
    layout.addWidget(widget)

    widget = QCheckBox("Check me")
    widget.setChecked(False)
    layout.addWidget(widget)

    widget = ControlRow()
    layout.addWidget(widget)

    main_window.setLayout(layout)
    main_window.show()

    app.exec()

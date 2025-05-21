from components import (ConfigDateTime, ConfigDirectory, ConfigFileSelector,
                        ConfigMultilineTextBox, ConfigTextBox)
from PySide6.QtCore import QRegularExpression, Qt, Signal
from PySide6.QtGui import QRegularExpressionValidator, QTextOption
from PySide6.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QScrollArea,
                               QSizePolicy, QTextEdit, QVBoxLayout, QWidget)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iBenthos - PhotoTransect Tool")
        self.setGeometry(100, 100, 1200, 600)

        # Create a horizontal 3 pane layout
        self._main_layout = QHBoxLayout()

        # Left pane
        self._left_pane = QVBoxLayout()
        # self._left_pane.set
        self._input_dir_config = ConfigDirectory(self, label_text="Input photo directory")
        self._left_pane.addWidget(self._input_dir_config)
        self._gpx_file_config = ConfigFileSelector(self, label_text="GPX file",
                                                   name_filters=["GPX files (*.gpx)"])
        self._left_pane.addWidget(self._gpx_file_config)
        self._gps_photo_config = ConfigFileSelector(self, label_text="GPS Photo")
        self._left_pane.addWidget(self._gps_photo_config)

        self._main_layout.addLayout(self._left_pane)

        # Middle pane
        self._middle_pane = QVBoxLayout()
        label = QLabel("iFDO details")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._middle_pane.addWidget(label)
        self._image_set_name = ConfigTextBox(self)
        self._image_set_name.label = "Image set name"
        self._image_set_name.defaultValue = "i.e. Site and date identifier"
        self._middle_pane.addWidget(self._image_set_name)

        self._main_layout.addLayout(self._middle_pane)

        # Right pane
        self._right_pane = QVBoxLayout()
        label = QLabel("Right Pane")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._right_pane.addWidget(label)

        self._main_layout.addLayout(self._right_pane)


        # Set the layout for the main window
        self.setLayout(self._main_layout)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
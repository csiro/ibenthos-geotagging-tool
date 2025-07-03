"""
main.py: Main entry point for the iBenthos Geotagging Tool application.
This script initializes the application, sets up the main controller, and starts the Qt event loop.

Copyright (c) 2025
Commonwealth Scientific and Industrial Research Organisation (CSIRO)
ABN 41 687 119 230

Author: Brendan Do <brendan.do@csiro.au>
"""
import logging
import os
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

import controller
import models
import views

logger = logging.getLogger(__name__)

def _get_runtime_variables():
    """
    Get runtime variables.
    
    Returns:
        A tuple containing the runtime variables. (exftool_path, build_id, version)
    """

    prod_mode = getattr(sys, "frozen", False)

    if prod_mode:
        # Running as a package
        app_path = Path(sys._MEIPASS) # pylint: disable=protected-access

        # Get exiftool_path based on platform
        match sys.platform:
            case "win32":
                _exiftool_path = str(app_path / "bin" / "exiftool.exe")
            case "darwin":
                _exiftool_path = str(app_path / "bin" / "exiftool")
            case _:
                raise NotImplementedError(
                                f"This platform is not currently supported: {sys.platform}")

        # Read the git hash from the build_id.txt file
        build_id_path = app_path / "build_id.txt"
        _build_id = "0"
        if build_id_path.exists():
            with open(build_id_path, "r", encoding="utf-8") as f:
                _build_id = f.read().strip()
            logger.info("Build ID: %s", _build_id)
        else:
            logger.warning("Build ID file not found.")

        # Read the version from the version.txt file
        version_path = app_path / "version.txt"
        _version = "0.0.0"
        if version_path.exists():
            with open(version_path, "r", encoding="utf-8") as f:
                _version = f.read().strip()
            logger.info("Version: %s", _version)
        else:
            logger.warning("Version file not found.")
    else:
        # Running as a script
        app_path = Path(os.path.dirname(os.path.realpath(__file__)))

        # Get exiftool_path based on platform
        match sys.platform:
            case "win32":
                _exiftool_path = str(app_path / ".." / "exiftool-13.29_64" / "exiftool.exe")
            case "darwin":
                _exiftool_path = str(app_path / ".." / "Image-ExifTool-13.29" / "exiftool")
            case _:
                raise NotImplementedError(
                                f"This platform is not currently supported: {sys.platform}")
        _build_id = "development"
        _version = "development"

    return (_exiftool_path, _build_id, _version) # pylint: disable=used-before-assignment


if __name__ == "__main__":
    app = QApplication(sys.argv)

    user_input_model = models.UserInputModel()
    config_model = models.ConfigModel()
    feedback_model = models.FeedbackModel()

    main_view = views.MainWindow()

    exiftool_path, config_model.buildHash, config_model.version = _get_runtime_variables()


    controller = controller.MainController(app_view=main_view,
                                           model=user_input_model,
                                           config=config_model,
                                           feedback=feedback_model,
                                           exec_path=exiftool_path)

    main_view.show()
    sys.exit(app.exec())

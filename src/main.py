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

def _get_build_id(prod_mode: bool, app_path: Path) -> str:
    if prod_mode:
        # Running as a package
        try:
            with open(app_path / "build_id.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.warning("Build ID file not found in package.")
    return "development"

def _get_version(prod_mode: bool, app_path: Path) -> str:
    if prod_mode:
        # Running as a package
        try:
            with open(app_path / "version.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.warning("Version file not found in package.")
    return "development"

def _get_exiftool_path(prod_mode: bool, app_path: Path) -> str:
    if sys.platform not in {"win32", "darwin"}:
        raise NotImplementedError(
            f"This platform is not currently supported: {sys.platform}")

    exe_name = "exiftool.exe" if sys.platform == "win32" else "exiftool"

    # Running as a package
    if prod_mode:
        return str(app_path / "bin" / exe_name)

    # Running as a script
    subdir = "exiftool-13.29_64" if sys.platform == "win32" else "Image-ExifTool-13.29"
    return str(app_path / ".." / subdir / exe_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    user_input_model = models.UserInputModel()
    config_model = models.ConfigModel()
    feedback_model = models.FeedbackModel()

    main_view = views.MainWindow()

    # Determine if we're running in production mode or not
    MODE = getattr(sys, "frozen", False)
    application_path = Path(sys._MEIPASS) if MODE else \
                       Path(os.path.dirname(os.path.realpath(__file__))) # pylint: disable=protected-access

    config_model.buildHash = _get_build_id(MODE, application_path)
    config_model.version = _get_version(MODE, application_path)

    controller = controller.MainController(app_view=main_view,
                                           model=user_input_model,
                                           config=config_model,
                                           feedback=feedback_model,
                                           exec_path=_get_exiftool_path(MODE, application_path))

    main_view.show()
    sys.exit(app.exec())

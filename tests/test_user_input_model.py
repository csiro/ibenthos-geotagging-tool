from pathlib import Path

import pytest

from src.models import UserInputModel, UserInputModelValidator


def valid_user_input_model() -> UserInputModel:
    user_input_model = UserInputModel()
    user_input_model.importDirectory = "file://" + str(Path(__file__).parent / "dataset")
    user_input_model.gpxFilepath = user_input_model.importDirectory + "/test.gpx"
    user_input_model.gpsPhotoFilepath = user_input_model.importDirectory + "/test.jpg"
    user_input_model.gpsDate = "2023-06-16"
    user_input_model.gpsTime = "08:37:36"
    user_input_model.gpsTimezoneIndex = 0
    user_input_model.exportDirectory = "file://" + str(Path(__file__).parent / "export")
    return user_input_model

def test_validator_valid_user_input_model():
    user_input_model = valid_user_input_model()
    validator = UserInputModelValidator()
    assert validator.validate(user_input_model) is True,\
           "Validator should return True for valid user input model"

def test_validator_import_directory():
    user_input_model = valid_user_input_model()
    validator = UserInputModelValidator()

    # Test for no import directory
    user_input_model.importDirectory = ""
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for empty import directory"

    # Test for invalid import directory
    user_input_model.importDirectory = "file:///invalid_directory"
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for invalid import directory"

    # Test for import directory not starting with 'file://'
    user_input_model = valid_user_input_model()
    user_input_model.importDirectory = user_input_model.importDirectory.replace("file://", "")
    assert validator.validate(user_input_model) is True,\
           "Validator should return True for import directory not starting with 'file://'"

    # Test for import directory not being a directory
    user_input_model.importDirectory = "file://" + str(Path(__file__).parent / "dataset/test.jpg")
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for import directory not being a directory"

def test_validator_gpx_filepath():
    user_input_model = valid_user_input_model()
    validator = UserInputModelValidator()

    # Test for no GPX file path
    user_input_model.gpxFilepath = ""
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for empty GPX file path"

    # Test for invalid GPX file path
    user_input_model.gpxFilepath = "file:///invalid_file.gpx"
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for invalid GPX file path"

    # Test for GPX file path not starting with 'file://'
    user_input_model = valid_user_input_model()
    user_input_model.gpxFilepath = user_input_model.gpxFilepath.replace("file://", "")
    assert validator.validate(user_input_model) is True,\
           "Validator should return True for GPX file path not starting with 'file://'"

    # Test for GPX file path not being a file
    user_input_model.gpxFilepath = "file://" + str(Path(__file__).parent / "dataset")
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for GPX file path not being a file"

def test_validator_gps_photo_filepath():
    user_input_model = valid_user_input_model()
    validator = UserInputModelValidator()

    # Test for no GPS photo file path
    user_input_model.gpsPhotoFilepath = ""
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for empty GPS photo file path"

    # Test for invalid GPS photo file path
    user_input_model.gpsPhotoFilepath = "file:///invalid_file.jpg"
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for invalid GPS photo file path"

    # Test for GPS photo file path not starting with 'file://'
    user_input_model = valid_user_input_model()
    user_input_model.gpsPhotoFilepath = user_input_model.gpsPhotoFilepath.replace("file://", "")
    assert validator.validate(user_input_model) is True,\
           "Validator should return True for GPS photo file path not starting with 'file://'"

    # Test for GPS photo file path not being a file
    user_input_model.gpsPhotoFilepath = "file://" + str(Path(__file__).parent / "dataset")
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for GPS photo file path not being a file"

def test_validator_gps_date():
    user_input_model = valid_user_input_model()
    validator = UserInputModelValidator()

    # Test for empty GPS date
    user_input_model.gpsDate = ""
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for empty GPS date"

    # Test for date in wrong format
    user_input_model.gpsDate = "2023-6-1"
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for GPS date in wrong format"

def test_validator_gps_time():
    user_input_model = valid_user_input_model()
    validator = UserInputModelValidator()

    # Test for empty GPS time
    user_input_model.gpsTime = ""
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for empty GPS time"

    # Test for time in wrong format
    user_input_model.gpsTime = "8:37"
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for GPS time in wrong format"

def test_validator_output_directory():
    user_input_model = valid_user_input_model()
    validator = UserInputModelValidator()

    # Test for no export directory
    user_input_model.exportDirectory = ""
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for empty export directory"

    # Test for invalid export directory
    user_input_model.exportDirectory = "file:///invalid_directory"
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for invalid export directory"

    # Test for export directory not starting with 'file://'
    user_input_model = valid_user_input_model()
    user_input_model.exportDirectory = user_input_model.exportDirectory.replace("file://", "")
    assert validator.validate(user_input_model) is True,\
           "Validator should return True for export directory not starting with 'file://'"

    # Test for export directory not being a directory
    user_input_model.exportDirectory = "file://" + str(Path(__file__).parent / "dataset/test.jpg")
    assert validator.validate(user_input_model) is False,\
           "Validator should return False for export directory not being a directory"

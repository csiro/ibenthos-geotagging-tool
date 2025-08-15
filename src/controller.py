"""
controller.py: Module provides the main controller for the geotagging tool.

Copyright (c) 2025
Commonwealth Scientific and Industrial Research Organisation (CSIRO)
ABN 41 687 119 230

Author: Brendan Do <brendan.do@csiro.au>
"""

import copy
import datetime
import hashlib
import logging
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from exiftool import ExifToolHelper
from geotag_pt import PhotoTransectGPSTagger
from PySide6.QtCore import QObject, QThread, Signal, Slot

import models
import views
from ifdo import IFDOModel
from imagekmlgen import ImageKMLGenerator
from timezones import TIMEZONES, Timezone

logger = logging.getLogger(__name__)

def _get_images(directory: Path):
    extensions = ['.jpg', '.jpeg', '.png']
    if not directory.exists() or not directory.is_dir():
        return []
    file_list = list(directory.rglob("*"))
    return [file for file in file_list if file.suffix.lower() in extensions]

@dataclass
class GeotagWorkerConfig:
    """
    Configuration for the geotagging worker.
    """
    # pylint: disable=too-many-instance-attributes
    # Configuration options will always be plentiful, so this is acceptable.
    tagger: PhotoTransectGPSTagger
    import_dir: Path
    export_dir: Path
    ifdo_model: IFDOModel | None = None
    exiftool_exec_path: str | None = None
    tz_override: str | None = None
    kml_export: bool = False
    base_tags: dict = field(default_factory=dict)

class GeotagWorker(QObject):
    """
    Worker class that contains the geotagging logic intended to be run as a separate thread.
    """
    progress = Signal(int, int)
    error_msgs = Signal(str)
    finished = Signal(str)

    def __init__(self, config: GeotagWorkerConfig):
        super().__init__()
        self.config = config

    def add_to_ifdo(self, relative_fn: str, exif_data: dict, gps_tags: dict):
        """
        Add image properties to the IFDO model.
        """
        if self.config.ifdo_model is None:
            return
        # Extract metadata required for IFDO model
        image_datetime = datetime.datetime.strptime(f'{gps_tags["Exif:GPSDateStamp"]} ' + \
                                                    f'{gps_tags["Exif:GPSTimeStamp"]}',
                                                    '%Y:%m:%d %H:%M:%S')\
                                                    .replace(tzinfo=datetime.UTC)
        image_latitude = float(gps_tags["Composite:GPSPosition"].split(" ")[0])
        image_longitude = float(gps_tags["Composite:GPSPosition"].split(" ")[1])
        if 'EXIF:Make' in exif_data and 'EXIF:Model' in exif_data:
            image_platform = f"{exif_data['EXIF:Make']} {exif_data['EXIF:Model']}"
        else:
            image_platform = "Unknown"

        # Calculate SHA256 hash of the image file
        hasher = hashlib.sha256()
        with open(self.config.export_dir / relative_fn, 'rb') as image_file:
            while chunk := image_file.read(1_048_576):  # 1MB chunks
                hasher.update(chunk)
        image_hash_sha256 = hasher.hexdigest()

        # Add the image properties to the IFDO model
        self.config.ifdo_model.add_image_properties(
            image_relative_path=str(relative_fn),
            image_datetime=image_datetime,
            image_latitude=image_latitude,
            image_longitude=image_longitude,
            image_platform=image_platform,
            image_sensor="Unknown",
            image_hash_sha256=image_hash_sha256
        )

    def _process_image(self, image_fn: Path, et: ExifToolHelper, 
                             kml_gen: ImageKMLGenerator | None = None):
        relative_fn = image_fn.relative_to(self.config.import_dir)
        exif_data = et.get_metadata(str(image_fn))[0]
        new_exif_tags = copy.copy(self.config.base_tags)

        # Generate GPS tags based on the EXIF data and the GPX file
        try:
            new_exif_tags |= self.config.tagger.generate_gps_tags(exif_data,
                                                        tz_override=self.config.tz_override)
        except IndexError as e:
            logger.error(
                "Image %s not within range of GPX file. Skipping this image.", image_fn
            )
            self.error_msgs.emit(
                f"Image {image_fn} not within range of GPX file. Skipping this image."
            )
            logger.error(e)
            return
        except AssertionError as _:
            logger.error(
                "Image %s does not contain time data. Skipping this image.", image_fn
            )
            self.error_msgs.emit(
                f"Image {image_fn} does not contain time data. Skipping this image."
            )
            return

        # Save the image with the new EXIF tags
        save_fn = self.config.export_dir / relative_fn
        save_fn.parent.mkdir(parents=True, exist_ok=True)
        if not save_fn.parent.exists():
            logger.error("Failed to create directory %s", save_fn.parent)
            return
        shutil.copy2(image_fn, save_fn)
        et.set_tags(files=save_fn, tags=new_exif_tags, params=['-overwrite_original'])

        # Add to IFDO model if enabled
        if self.config.ifdo_model is not None:
            self.add_to_ifdo(relative_fn, exif_data, new_exif_tags)

        # Add to KML generator if enabled
        if kml_gen:
            try:
                kml_gen.add_image_point(save_fn)
            except KeyError as e:
                logger.error("Missing GPS data in image %s: %s", image_fn, e)
                self.error_msgs.emit(f"Missing GPS data in image {image_fn}: {e}")
        logger.info("Image %s geotagged and saved to %s", image_fn, save_fn)

    def run(self):
        """
        Runs the geotagging process.
        """
        # Get images to be tagged
        image_list = _get_images(self.config.import_dir)

        total_images = len(image_list)

        kml_gen = ImageKMLGenerator(self.config.export_dir) if self.config.kml_export else None

        with ExifToolHelper(executable=self.config.exiftool_exec_path) as et:
            for idx, image_fn in enumerate(image_list):
                self._process_image(image_fn, et, kml_gen)
                self.progress.emit(idx, total_images)
        # Save the IFDO model to a file
        if self.config.ifdo_model is not None:
            ifdo_path = self.config.export_dir / "ifdo.yml"
            self.config.ifdo_model.export_ifdo_yaml(str(ifdo_path))
            logger.info("IFDO file saved to %s", ifdo_path)

        # Save KML file if required
        if kml_gen:
            kml_gen.save()
            logger.info("KML file saved to %s", self.config.export_dir / 'images.kmz')
        self.finished.emit("Finished geotagging images.")

class MainController(QObject):
    """
    Main controller that handles the interaction between the view and the model.
    """
    def __init__(self, app_view: views.MainWindow, model: models.UserInputModel,
                 config: models.ConfigModel, feedback: models.FeedbackModel,
                 exec_path: str | None = None):
        super().__init__()
        self._app_view = app_view
        self._model = model
        self._config = config
        self._feedback = feedback
        self._worker = None
        self._workerthread = None
        self._exec_path = exec_path

        # Set the timezone options
        self._config.gpsTimezoneOptions = TIMEZONES

        # Connect the signals from the view to the model
        model_to_view_signal_map = {
            'importDirectory': self._app_view.inputDirChanged,
            'gpxFilepath': self._app_view.gpxFileChanged,
            'gpsPhotoAvailable': self._app_view.gpsPhotoAvailableChanged,
            'gpsPhotoFilepath': self._app_view.gpsPhotoChanged,
            'gpsDate': self._app_view.gpsDateChanged,
            'gpsTime': self._app_view.gpsTimeChanged,
            'gpsTimezoneIndex': self._app_view.gpsTimezoneIndexChanged,
            'cameraTimezoneIndex': self._app_view.cameraTimezoneIndexChanged,
            'exportDirectory': self._app_view.outputDirChanged,
            'ifdoEnable': self._app_view.ifdoExportChanged,
            'imageSetName': self._app_view.imageSetNameChanged,
            'imageContext': self._app_view.contextChanged,
            'projectName': self._app_view.projectNameChanged,
            'eventName': self._app_view.eventNameChanged,
            'piName': self._app_view.piNameChanged,
            'piORCID': self._app_view.piOrcidChanged,
            'collectorName': self._app_view.collectorNameChanged,
            'collectorORCID': self._app_view.collectorOrcidChanged,
            'organisation': self._app_view.copyrightOwnerChanged,
            'license': self._app_view.licenseChanged,
            'distanceAboveGround': self._app_view.distanceAGChanged,
            'imageAbstract': self._app_view.imageAbstractChanged,
            'exportKML': self._app_view.kmlExportChanged,
            'attributionExport': self._app_view.attributionExportChanged
        }

        def _make_model_updater(attr):
            return lambda x: setattr(self._model, attr, x)

        for model_attr, view_signal in model_to_view_signal_map.items():
            view_signal.connect(_make_model_updater(model_attr))

        # Connect processing logic
        self._app_view.startProcessingTriggered.connect(self.run_geotagging_process)

        # Connect internal view logic
        self._app_view.clearFormTriggered.connect(self._app_view.clearForm)
        self._app_view.inputDirChanged.connect(self._app_view.setDefaultPath)
        self._app_view.attributionExportChanged.connect(\
            self._app_view.enableDisableAttributionFields)
        self._app_view.ifdoExportChanged.connect(self._app_view.enableDisableIFDODetails)
        self._app_view.gpsPhotoChanged.connect(self._app_view._image_preview.setFilepath)

        # Connect menu actions
        self._app_view.aboutTriggered.connect(self.show_about)
        self._app_view.documentationTriggered.connect(self._app_view.OpenDocumentationURL)

        # Set up configs into view
        default_window_title = self._app_view.windowTitle()
        self._app_view.setWindowTitle(f"{default_window_title} - v{self._config.version}")
        self._app_view.setTimezoneOptions(self._config.gpsTimezoneOptions)
        self._app_view.setTimezoneIndexDefault(15, reset=True)

        # Set up the feedback model into view
        self._feedback.feedbackTextChanged.connect(self._app_view.setFeedbackText)
        self._feedback.progressChanged.connect(self._app_view.setProgress)

    def _gen_attribution_tags(self):
        """
        Generate attribution tags for the images based on the user input.
        This is used to set common metadata for all images.
        """
        if self._model.collectorORCID != "":
            collector_str = f"{self._model.collectorName} " + \
            f"(Image collector, ORCID: {self._model.collectorORCID})"
        else:
            collector_str = f"{self._model.collectorName} (Image collector)"
        if self._model.piORCID != "":
            pi_str = f"{self._model.piName} " + \
            f"(Principal Investigator, ORCID: {self._model.piORCID})"
        else:
            pi_str = f"{self._model.piName} (Principal Investigator)"
        return {
            "Exif:Artist": f"{collector_str}; {pi_str}",
            "Creator": f"{collector_str}; {pi_str}",
            "Copyright": f"{self._model.organisation} (Licensed under {self._model.license})"
        }

    @staticmethod
    def _strip_file_url(file_path: str) -> str:
        return file_path.removeprefix("file://")

    def _create_geotagger(self, tz_override: str) -> PhotoTransectGPSTagger:
        # Use GPS photo and timestamp only if GPS photo is available
        jpg_gps_timestamp = None
        gps_photo_path = None
        if self._model.gpsPhotoAvailable:
            jpg_gps_timestamp = datetime.datetime.fromisoformat(
                self._model.gpsDate + " " + self._model.gpsTime
            )
            jpg_gps_timestamp = jpg_gps_timestamp.replace(tzinfo=Timezone(
                self._config.gpsTimezoneOptions[self._model.gpsTimezoneIndex])
            )
            gps_photo_path = self._strip_file_url(self._model.gpsPhotoFilepath)

        return PhotoTransectGPSTagger.from_files(
            self._strip_file_url(self._model.gpxFilepath),
            jpg_gps_fn=gps_photo_path,
            jpg_gps_timestamp=jpg_gps_timestamp,
            exiftool_path=self._exec_path,
            tz_override=tz_override
        )

    def _create_ifdo_model(self) -> IFDOModel | None:
        """
        Create an IFDO model based on the user input.
        Returns:
            IFDOModel: The created IFDO model or None if IFDO export is not enabled.
        """
        if not self._model.ifdoEnable:
            return None
        return IFDOModel(
            image_set_name=self._model.imageSetName,
            image_context=self._model.imageContext,
            image_project=self._model.projectName,
            image_event=self._model.eventName,
            image_pi=(self._model.piName, self._model.piORCID or "0000-0000-0000-0000"),
            image_creators=[(self._model.collectorName, self._model.collectorORCID or
                             "0000-0000-0000-0000")],
            image_copyright=self._model.organisation,
            image_license=self._model.license,
            image_abstract=self._model.imageAbstract,
            image_meters_above_ground=float(self._model.distanceAboveGround)
        )

    @Slot()
    def run_geotagging_process(self):
        """
        Slot intended to start the geotagging process.
        This method validates the user input, and starts the geotagging worker thread.
        """
        # Manually trigger field signals to update the model
        self._app_view.manuallyTriggerFieldSignals()

        # Clear any previous feedback
        self._feedback.feedbackText = ""
        # Validate the input
        validator = models.UserInputModelValidator()
        self._feedback.feedbackText = "Validating input...\n"
        if not validator.validate(self._model):
            self._feedback.addFeedbackLine("Validation failed")
            for error in validator.latest_errors:
                self._feedback.addFeedbackLine(error)
            return

        # Define the timezone override based on the camera timezone index
        tz_override = self._config.gpsTimezoneOptions[self._model.cameraTimezoneIndex]\
                          .replace("UTC", "")

        # Create the PhotoTransectGPSTagger object
        tagger = self._create_geotagger(tz_override)

        # Create the IFDO model
        ifdo_model = self._create_ifdo_model()

        # Create new worker thread
        self._workerthread = QThread()
        import_dir = Path(self._strip_file_url(self._model.importDirectory))
        export_dir = Path(self._strip_file_url(self._model.exportDirectory))
        worker_config = GeotagWorkerConfig(
            tagger=tagger,
            import_dir=import_dir,
            export_dir=export_dir,
            ifdo_model=ifdo_model,
            exiftool_exec_path=self._exec_path,
            tz_override=tz_override,
            kml_export=self._model.exportKML,
            base_tags=self._gen_attribution_tags() if self._model.attributionExport else {}
        )
        self._worker = GeotagWorker(worker_config)

        # Move the worker to the thread and connect signals
        self._worker.moveToThread(self._workerthread)
        self._workerthread.started.connect(self._worker.run)
        self._worker.progress.connect(self._feedback.updateProgress)
        self._worker.finished.connect(self._workerthread.quit)
        self._worker.error_msgs.connect(self._feedback.addFeedbackLine)
        self._worker.finished.connect(self._feedback.addFeedbackLine)
        self._worker.finished.connect(self._worker.deleteLater)
        self._workerthread.finished.connect(self._workerthread.deleteLater)

        # This ensures the progress bar fills up once execution completes
        self._workerthread.finished.connect(lambda : self._app_view.setProgress(100))

        # Start worker thread and update the UI
        self._workerthread.start()
        if self._model.gpsPhotoAvailable:
            self._feedback.addFeedbackLine("Geotagging images using GPS photo synchronization...")
        else:
            self._feedback.addFeedbackLine("Geotagging images assuming camera and GPS times "
                                           "are synchronized...")
        self._feedback.addFeedbackLine("Processing images...")

    @Slot()
    def show_about(self):
        """Show the About dialog with version and build information."""
        self._app_view.showAboutDialog(
            version=self._config.version,
            build_hash=self._config.buildHash
        )

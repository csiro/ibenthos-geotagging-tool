import logging
import pathlib
from string import Template
from typing import Optional, Tuple

import simplekml
from PIL import ExifTags, Image

LOGGER = logging.getLogger(__name__)

def _dms_to_decimal(polarity: str, degrees: int, minutes: int, seconds: float) -> float:
        """
        Convert DMS (Degrees, Minutes, Seconds) to decimal degrees.
        Polarity is either 'N', 'S', 'E', or 'W'.
        """
        decimal = degrees + (minutes / 60) + (seconds / 3600)
        if polarity in ['S', 'W']:
            decimal *= -1
        return float(decimal)

class ImageKMLGenerator:
    def __init__(self, output_directory: pathlib.Path):
        self._kml = simplekml.Kml()
        self._output_directory = output_directory
        self._image_template = Template(
            '<img src="$image_relative_path" style="max-width: ${max_width}px;"/>'
        )
    
    def add_image_point(self, image_path, name: str = None,
                              max_width: int = 400,
                              coordinates: Optional[Tuple[float, float]] = None):
        """
        Add a point to the KML file which contains the image in the description.
        Uses the image's GPS EXIF data to set the coordinates (lon, lat) if not provided.

        Raises FileNotFoundError if the image file does not exist.
        Raises KeyError if image does not have GPS data associated with it.
        """
        if name is None:
            name = pathlib.Path(image_path).stem
        
        # Open the image to get the resolution and if required, GPS coordinates
        with Image.open(image_path) as img:
            width, height = img.size
            
            if coordinates is None:
                # Attempt to extract GPS coordinates from the image EXIF data
                exif_data = img.getexif()
                gps_ifd = exif_data.get_ifd(ExifTags.IFD.GPSInfo)
                coordinates = (
                     _dms_to_decimal(
                        gps_ifd[ExifTags.GPS.GPSLongitudeRef],
                        *gps_ifd[ExifTags.GPS.GPSLongitude]
                     ),
                     _dms_to_decimal(
                        gps_ifd[ExifTags.GPS.GPSLatitudeRef],
                        *gps_ifd[ExifTags.GPS.GPSLatitude]
                     )
                )
        
        # Add the point to the KML
        point = self._kml.newpoint(name=name, coords=[coordinates],
                                   description=self._image_template.substitute(
                                        image_relative_path=pathlib.Path(image_path).relative_to(self._output_directory),
                                        max_width=max_width,
                                        visibility=0
                                   ))
        point.style = simplekml.Style()
        point.style.iconstyle.icon.href = "https://www.iconsdb.com/icons/download/white/circle-48.png"
        point.style.iconstyle.scale = 0.5
        point.style.iconstyle.color = simplekml.Color.green

    def save(self):
        """
        Save the KML file.
        """
        self._kml.save(self._output_directory / 'images.kml')
        LOGGER.info(f"KML file saved to {self._output_directory / 'images.kml'}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate KML file from images with GPS data.")
    parser.add_argument('directory', type=pathlib.Path, help="Directory with geotagged images.")
    args = parser.parse_args()

    kmlgen = ImageKMLGenerator(args.directory)

    for image_file in args.directory.glob('*.[Jj][Pp][Gg]'):
        try:
            kmlgen.add_image_point(image_file)
        except KeyError as e:
            LOGGER.error(f"Missing GPS data in image {image_file}: {e}")
    kmlgen.save()
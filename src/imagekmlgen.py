"""
imagekmlgen.py: This module provides functionality to generate KML/KMZ files
from images with GPS data. It supports generating circular thumbnails for images
and includes them in the KML/KMZ file.

Copyright (c) 2025
Commonwealth Scientific and Industrial Research Organisation (CSIRO)
ABN 41 687 119 230

Author: Brendan Do <brendan.do@csiro.au>
"""
import logging
import pathlib
import zipfile
from io import BytesIO
from string import Template

import simplekml
from PIL import ExifTags, Image, ImageDraw

LOGGER = logging.getLogger(__name__)

def _dms_to_decimal(polarity: str, degrees: int, minutes: int, seconds: float) -> float:
    """
    Convert DMS (Degrees, Minutes, Seconds) to decimal degrees.
    Polarity is either 'N', 'S', 'E', or 'W'.

    Args:
        polarity: 'N' or 'S' for latitude, 'E' or 'W' for longitude
        degrees: Degrees part of the DMS
        minutes: Minutes part of the DMS
        seconds: Seconds part of the DMS

    Returns:
        Decimal representation of the coordinates.
    """
    decimal = degrees + (minutes / 60) + (seconds / 3600)
    if polarity in ['S', 'W']:
        decimal *= -1
    return float(decimal)

def _generate_circular_thumbnail(image: Image.Image, size: int = 128, border_size: int = 3)\
    -> Image.Image:
    """
    Generate a circular thumbnail of the given image with white border.
    
    Args:
        image: The input image to create a thumbnail from
        size: The size of the output thumbnail (default: 128px)
        border_size: The width of the white border in pixels (default: 3px)
    
    Returns:
        A PIL.Image.Image object representing the circular thumbnail
    """
    # Create a square thumbnail centred on the image
    image = image.crop(((image.size[0] - min(image.size)) // 2,
                        (image.size[1] - min(image.size)) // 2,
                        (image.size[0] + min(image.size)) // 2,
                        (image.size[1] + min(image.size)) // 2))

    if border_size > 0:
        # Create a mask for the inner circular area
        inner_size = size - (2 * border_size)
        inner_mask = Image.new('L', (inner_size, inner_size), 0)
        inner_draw = ImageDraw.Draw(inner_mask)
        inner_draw.ellipse((0, 0, inner_size, inner_size), fill=255)

        image.thumbnail((size - 2 * border_size, size - 2 * border_size), Image.Resampling.LANCZOS)
    else:
        image.thumbnail((size, size), Image.Resampling.LANCZOS)

    # Create a mask for the circular thumbnail
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    # Create the final thumbnail with transparent background
    circular_thumbnail = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    # Add the image to the circular thumbnail
    if border_size > 0:
        # Generate a white circular image, and then paste the image on top
        white_image = Image.new('RGBA', (size, size), color='white')
        circular_thumbnail.paste(white_image, (0, 0), mask)
        circular_thumbnail.paste(image, (border_size, border_size), inner_mask)
    else:
        circular_thumbnail.paste(image, (0, 0), mask)

    return circular_thumbnail

class ImageKMLGenerator:
    """
    A class used to generate a KML or KMZ file with points which represent images with GPS data.
    """
    def __init__(self, output_directory: pathlib.Path, preview_thumbnail: bool = True):
        self._kml = simplekml.Kml()
        self._output_directory = output_directory
        self._image_template = Template(
            '<p>$name</p><img src="$image_relative_path" style="max-width: ${max_width}px;"/>'
        )
        self._generate_preview_thumbnail = preview_thumbnail
        self._thumbnails = {}

    def _generate_point_style(self, point: simplekml.Point, thumbnail_path: str | None = None):
        """
        Generate the style for a point in the KML file.

        Args:
            point: The simplekml.Point object to style.
            thumbnail_path: Optional path to a thumbnail image to use as the icon.
                            If not provided, a default icon will be used.
        """
        if thumbnail_path:
            point.stylemap.normalstyle.iconstyle.icon.href = thumbnail_path
            point.stylemap.normalstyle.iconstyle.scale = 1.0
            point.stylemap.normalstyle.labelstyle.scale = 0
            point.stylemap.highlightstyle.iconstyle.icon.href = thumbnail_path
            point.stylemap.highlightstyle.iconstyle.scale = 1.5
            point.stylemap.highlightstyle.labelstyle.scale = 1
        else:
            point.stylemap.normalstyle.iconstyle.icon.href = \
                "https://www.iconsdb.com/icons/download/white/circle-48.png"
            point.stylemap.normalstyle.iconstyle.scale = 1.0
            point.stylemap.normalstyle.iconstyle.color = simplekml.Color.green
            point.stylemap.normalstyle.labelstyle.scale = 0
            point.stylemap.highlightstyle.iconstyle.icon.href = \
                "https://www.iconsdb.com/icons/download/white/circle-48.png"
            point.stylemap.highlightstyle.iconstyle.scale = 1.5
            point.stylemap.highlightstyle.iconstyle.color = simplekml.Color.green
            point.stylemap.highlightstyle.labelstyle.scale = 1

    def add_image_point(self, image_path, name: str = None,
                              max_width: int = 400,
                              coordinates: tuple[float, float] | None = None):
        """
        Add a point to the KML file which contains the image in the description.
        Uses the image's GPS EXIF data to set the coordinates (lon, lat) if not provided.

        Args:
            image_path: Path to the image file.
            name: Optional name for the point. If not provided, the image file name is used.
            max_width: Maximum width of the image in the KML description.
            coordinates: Optional tuple of (longitude, latitude). If not provided, method will 
                         attempt to extract GPS coordinates from the image's EXIF data.
        
        Raises:
            FileNotFoundError: if the image file does not exist.
            KeyError: if image does not have GPS data associated with it and coordinates not 
                      provided.
        """
        if name is None:
            name = pathlib.Path(image_path).stem

        # Open the image to get the resolution and if required, GPS coordinates
        with Image.open(image_path) as img:
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
            thumbnail_path = None
            if self._generate_preview_thumbnail:
                # Generate a circular thumbnail of the image
                thumbnail = _generate_circular_thumbnail(img)
                thumbnail_path = f".thumbs/{name}.png"

                # Stick in memory for now, save to disk when save requested
                self._thumbnails[thumbnail_path] = thumbnail


        # Add the point to the KML
        point = self._kml.newpoint(name=name, coords=[coordinates],
                                   description=self._image_template.substitute(
                                        name=name,
                                        image_relative_path=pathlib.Path(image_path)\
                                                            .relative_to(self._output_directory),
                                        max_width=max_width
                                   ), visibility=0)
        # Set the point's style
        self._generate_point_style(point, thumbnail_path)

    def save(self):
        """
        Save the KML file.
        """
        if not self._generate_preview_thumbnail:
            self._kml.save(self._output_directory / 'images.kml')
            LOGGER.info("KML file saved to %s", self._output_directory / 'images.kml')
        else:
            # Get the KML string representation
            kml_string = self._kml.kml()

            # Write the KML file and thumbnails to a KMZ file
            with zipfile.ZipFile(self._output_directory / 'images.kmz', 'w', zipfile.ZIP_DEFLATED) \
                as kml_zip:
                # Write the KML file
                kml_zip.writestr('doc.kml', kml_string)

                # Write all thumbnails to the zip file
                for thumbnail_path, thumbnail in self._thumbnails.items():
                    with BytesIO() as bytes_io:
                        thumbnail.save(bytes_io, format='PNG')
                        kml_zip.writestr(thumbnail_path, bytes_io.getvalue())
            LOGGER.info("KMZ file saved to %s", self._output_directory / 'images.kmz')


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
            LOGGER.error("Missing GPS data in image %s: %s", image_file, e)
    kmlgen.save()

'''
ifdo.py: Module provides minimal implementation of the image FAIR Digital Objects (iFDO) model.

Copyright (c) 2025
Commonwealth Scientific and Industrial Research Organisation (CSIRO)
ABN 41 687 119 230

Author: Brendan Do <brendan.do@csiro.au>
'''
import datetime
import uuid
from typing import Dict, List, Tuple

import yaml


class IFDOModel:
    """
    Minimal implementation of the image FAIR Digital Objects (iFDO) model.
    Implements core and some capture properties as per version v2.1.0 of iFDO specification.
    """
    def __init__(self,
        image_set_name: str,
        image_context: str,
        image_project: str,
        image_event: str,
        image_pi: Tuple[str, str],
        image_creators: List[Tuple[str,str]],
        image_copyright: str,
        image_abstract: str,
        image_altitude_meters: float = 0.0,
        image_license: str = "CC BY 4.0",
        image_acquisition: str = "photo",
        image_quality: str = "processed",
        image_deployment: str = "survey",
        image_navigation: str = "satellite",
        image_meters_above_ground: float = 0.9,
        image_target_environment: str = "Shallow Benthic"
    ):
        self.image_set_uuid = str(uuid.uuid4())
        self.images = {}

        self.image_set_name = image_set_name
        self.image_altitude_meters = image_altitude_meters
        self.image_context = image_context
        self.image_project = image_project
        self.image_event = image_event
        self.image_pi = {'name': image_pi[0], 'orcid': image_pi[1]}
        self.image_creators = [{'name': x[0], 'orcid': x[1]} for x in image_creators]
        self.image_license = {'name': image_license}
        self.image_copyright = image_copyright
        self.image_abstract = image_abstract
        self.image_acquisition = image_acquisition
        self.image_quality = image_quality
        self.image_deployment = image_deployment
        self.image_navigation = image_navigation
        self.image_meters_above_ground = image_meters_above_ground
        self.image_target_environment = image_target_environment


    def add_image_properties(
        self,
        image_relative_path: str,
        image_datetime: datetime.datetime,
        image_latitude: float,
        image_longitude: float,
        image_platform: str,
        image_sensor: str,
        image_hash_sha256: str
    ):
        new_image = {}
        new_image['image-datetime'] = image_datetime.astimezone(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S.%f')
        new_image['image-latitude'] = image_latitude
        new_image['image-longitude'] = image_longitude
        new_image['image-altitude-meters'] = self.image_altitude_meters
        new_image['image-context'] = {'name': self.image_context}
        new_image['image-project'] = {'name': self.image_project}
        new_image['image-event'] = {'name': self.image_event}
        new_image['image-platform'] = {'name': image_platform}
        new_image['image-sensor'] = {'name': image_sensor}
        new_image['image-uuid'] = str(uuid.uuid4())
        new_image['image-hash-sha256'] = image_hash_sha256
        new_image['image-pi'] = self.image_pi
        new_image['image-creators'] = self.image_creators
        new_image['image-license'] = self.image_license
        new_image['image-copyright'] = self.image_copyright
        new_image['image-abstract'] = self.image_abstract
        new_image['image-acquisition'] = self.image_acquisition
        new_image['image-quality'] = self.image_quality
        new_image['image-deployment'] = self.image_deployment
        new_image['image-navigation'] = self.image_navigation
        new_image['image-meters-above-ground'] = self.image_meters_above_ground
        new_image['image-target-environment'] = self.image_target_environment

        self.images[image_relative_path] = [new_image]

    def export_ifdo_dict(self) -> Dict:
        output = {}
        output['image-set-header'] = {}
        output['image-set-header']['image-set-uuid'] = self.image_set_uuid
        output['image-set-header']['image-set-name'] = self.image_set_name
        output['image-set-header']['image-set-handle'] = ''
        output['image-set-header']['image-set-ifdo-version'] = 'v2.1.0'
        output['image-set-items'] = self.images
        return output

    def export_ifdo_yaml(self, output_path: str) -> None:
        with open(output_path, 'w', encoding='utf-8') as f:
            # Set up pyyaml to not use aliases
            # https://stackoverflow.com/a/30682604
            yaml.Dumper.ignore_aliases = lambda *args: True
            yaml.dump(self.export_ifdo_dict(), f, allow_unicode=True, sort_keys=False,
                      Dumper=yaml.Dumper)
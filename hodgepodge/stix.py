import collections
import json
import os
from typing import Iterable, Iterator, List, Optional

import uuid

from hodgepodge.constants import JSON_INDENT

DEFAULT_STIX_BUNDLE_FILENAME = 'stix2-bundle.json'

DEFAULT_INCLUDE_REVOKED = False
DEFAULT_INCLUDE_DEPRECATED = False

DEFAULT_REVOCATION_KEYS = [
    'revoked'
]

DEFAULT_DEPRECATION_KEYS = [
    'x-mitre-deprecated'
]

def expand_bundle_file(
        input_file: str, 
        output_dir: str,
        include_revoked: bool = DEFAULT_INCLUDE_REVOKED,
        include_deprecated: bool = DEFAULT_INCLUDE_DEPRECATED,
        revocation_keys: Iterable[str] = DEFAULT_REVOCATION_KEYS,
        deprecation_keys: Iterable[str] = DEFAULT_DEPRECATION_KEYS) -> List[dict]:
    """
    Expanding a STIX 2 bundle file into a directory consists of:
    
    - Reading STIX objects from the input file
    - Applying filters for revoked and deprecated objects
    - Writing the filtered set of STIX 2 objects to the output directory
    - Grouping objects by type (i.e. attack-pattern, course-of-action, etc.)
    - For each object type:
        - Generating a STIX 2 bundle file containing all objects of that type (e.g. attack-pattern/stix2-bundle.json)
        - Generating a STIX 2 bundle file for each individual object (e.g. attack-pattern/attack-pattern--1234.json)
    """
    objects = list(read_objects(
        path=input_file,
        include_revoked=include_revoked,
        include_deprecated=include_deprecated,
        revocation_keys=revocation_keys,
        deprecation_keys=deprecation_keys
    ))

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Copy the input file to the output directory
    output_file_path = os.path.join(output_dir, DEFAULT_STIX_BUNDLE_FILENAME)
    with open(output_file_path, 'w') as fp:
        for o in objects:
            json.dump(o, fp, indent=JSON_INDENT)
            fp.write('\n')

    # Group objects by type
    objects_by_type = collections.defaultdict(list)
    for o in objects:
        t = o['type']
        objects_by_type[t].append(o)
    
    for t, objects in objects_by_type.items():
        object_dir = os.path.join(output_dir, t)
        os.makedirs(object_dir, exist_ok=True)

        # Generate one STIX 2 bundle per object type
        output_path = os.path.join(object_dir, DEFAULT_STIX_BUNDLE_FILENAME)
        with open(output_path, 'w') as fp:
            bundle = new_bundle(objects)
            json.dump(bundle, fp, indent=JSON_INDENT)

        # Generate one STIX 2 bundle per object
        for o in objects:
            object_id = o['id']
            output_path = os.path.join(object_dir, f'{object_id}.json')
            with open(output_path, 'w') as fp:
                bundle = new_bundle([o])
                json.dump(bundle, fp, indent=JSON_INDENT)


def new_bundle_file(path: str, objects: List[dict]):
    bundle = new_bundle(objects)
    with open(path, 'w') as fp:
        json.dump(bundle, fp, indent=JSON_INDENT)


def new_bundle(objects: List[dict]) -> dict:
    return {
        'id': f'bundle--{uuid.uuid4()}',
        'type': 'bundle',
        'objects': sorted(objects, key=lambda o: (o['type'], o.get('name')))
    }


def read_objects(
        path: str, 
        include_revoked: bool = DEFAULT_INCLUDE_REVOKED, 
        include_deprecated: bool = DEFAULT_INCLUDE_DEPRECATED,
        revocation_keys: Optional[Iterable[str]] = None,
        deprecation_keys: Optional[Iterable[str]] = None) -> Iterator[dict]:

    if include_deprecated is False:
        deprecation_keys = deprecation_keys or DEFAULT_DEPRECATION_KEYS
    
    if include_revoked is False:
        revocation_keys = revocation_keys or DEFAULT_REVOCATION_KEYS

    with open(path) as fp:
        bundle = json.load(fp)
        for o in bundle['objects']:
            
            if include_revoked is False and any(k in o and o[k] for k in revocation_keys):
                continue

            if include_deprecated is False and any(k in o and o[k] for k in deprecation_keys):
                continue

            yield o

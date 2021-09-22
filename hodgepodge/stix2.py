from hodgepodge.exceptions import CompressionError
from stix2.datastore import DataSource, CompositeDataSource
from typing import List, Union, Optional, Iterator, Tuple, Any, Iterable

import hodgepodge.compression
import hodgepodge.files
import hodgepodge.patterns
import json
import logging
import stix2.datastore.memory
import taxii2client.v20

logger = logging.getLogger(__name__)

MITRE_ATTACK_ENTERPRISE_URL = 'https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e'
MITRE_ATTACK_MOBILE_URL = 'https://cti-taxii.mitre.org/stix/collections/2f669986-b40b-4423-b720-4396ca6a462b'
MITRE_ATTACK_ICS_URL = 'https://cti-taxii.mitre.org/stix/collections/02c3ef24-9cd4-48f3-a99f-b74ce24f1d34'

PUBLIC_TAXII_SERVICE_URLS = [
    MITRE_ATTACK_ENTERPRISE_URL,
    MITRE_ATTACK_MOBILE_URL,
    MITRE_ATTACK_ICS_URL,
]


def get_taxii_data_source(url, allow_custom: bool = True, items_per_page: int = 5000) -> stix2.TAXIICollectionSource:
    collection = taxii2client.v20.Collection(url)
    return stix2.TAXIICollectionSource(collection, allow_custom=allow_custom, items_per_page=items_per_page)


def get_filesystem_data_source(path: str, allow_custom: bool = True) -> Union[stix2.MemorySource, stix2.FileSystemSource]:
    if not hodgepodge.files.exists(path):
        raise FileNotFoundError(path)

    if hodgepodge.files.is_directory(path):
        return _get_data_source_from_directory(path=path, allow_custom=allow_custom)
    else:
        return _get_data_source_from_file(path=path, allow_custom=allow_custom)


def _get_data_source_from_file(path: str, allow_custom: bool = True) -> stix2.MemorySource:
    with open(path, 'rb') as fp:
        data = fp.read()
        try:
            data = hodgepodge.compression.decompress(data)
        except CompressionError as e:
            logger.debug("Data is either not compressed, or decompression failed: %s", e)
        return stix2.MemorySource(data, allow_custom=allow_custom)


def _get_data_source_from_directory(path: str, allow_custom: bool = True) -> stix2.FileSystemSource:
    return stix2.FileSystemSource(stix_dir=path, allow_custom=allow_custom)


def get_composite_data_source(paths: Iterable[str] = None, urls: Iterable[str] = None, allow_custom: bool = True) -> CompositeDataSource:
    if not (paths or urls):
        raise ValueError("At least one path or URL is required")

    data_sources = []

    if paths:
        for path in paths:
            data_source = get_filesystem_data_source(path=path, allow_custom=allow_custom)
            data_sources.append(data_source)

    if urls:
        for url in urls:
            data_source = get_taxii_data_source(url=url, allow_custom=allow_custom)
            data_sources.append(data_source)

    return combine_data_sources(data_sources)


def combine_data_sources(data_sources: Iterable[DataSource]) -> CompositeDataSource:
    src = CompositeDataSource()
    src.add_data_sources(list(data_sources))
    return src


def get_object(data_source: DataSource, object_id: str) -> Optional[dict]:
    row = data_source.get(stix_id=object_id)
    if row:
        return stix2_to_dict(row)


def get_objects(data_source: DataSource, object_ids: Iterable[str] = None, object_external_ids: Iterable[str] = None,
                object_types: Iterable[str] = None, object_names: Iterable[str] = None) -> List[dict]:

    return list(iter_objects(
        data_source=data_source,
        object_ids=object_ids,
        object_external_ids=object_external_ids,
        object_types=object_types,
        object_names=object_names,
    ))


def iter_objects(data_source: DataSource, object_ids: Iterable[str] = None, object_external_ids: Iterable[str] = None,
                 object_types: Iterable[str] = None, object_names: Iterable[str] = None) -> Iterator[dict]:

    constraints = []

    #: Filter objects by (internal) ID.
    if object_ids:
        constraint = ('id', 'in', object_ids)
        constraints.append(constraint)

    #: Filter objects by type.
    if object_types:
        constraint = ('type', 'in', object_types)
        constraints.append(constraint)

    #: Execute the query.
    for row in query(data_source=data_source, constraints=constraints):
        row = stix2_to_dict(row)

        #: Filter objects by name or alias - doing this here allows us to support regular expressions and globs.
        if object_names:
            if 'name' not in row:
                continue

            names = [row['name']] + row.get('aliases', [])
            if not hodgepodge.patterns.str_matches_glob(values=names, patterns=object_names):
                continue

        #: Filter objects by external ID - performing this operation on the server-side appears to be broken. :(
        if object_external_ids:
            external_ids = {ref['external_id'] for ref in row.get('external_references', []) if 'external_id' in ref}
            if set(object_external_ids).isdisjoint(external_ids):
                continue

        yield row


def query(data_source: DataSource, constraints: List[Tuple[str, str, Any]] = None) -> Iterator[dict]:
    constraints = [stix2.Filter(k, o, v) for (k, o, v) in constraints]
    for row in data_source.query(constraints):
        yield stix2_to_dict(row)


def stix2_to_dict(data: Any) -> dict:
    if isinstance(data, dict):
        return data
    return json.loads(data.serialize())

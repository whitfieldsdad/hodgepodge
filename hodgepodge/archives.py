from typing import List
from hodgepodge.constants import VERBOSE_BY_DEFAULT

import hodgepodge.toolkits.host.file_search as file_search
import hodgepodge.files
import zipfile
import logging


logger = logging.getLogger(__name__)


def create_archive(input_paths: List[str], output_path: str, verbose: bool = VERBOSE_BY_DEFAULT):
    if verbose:
        logger.info("Creating archive %s -> %s", input_paths, output_path)

    #: Resolve the "real" location of any input files.
    input_paths = file_search.resolve_paths(input_paths)
    if not any(hodgepodge.files.exists(path) for path in input_paths):
        raise FileNotFoundError(input_paths)

    #: Create the archive.
    with zipfile.ZipFile(output_path, 'w') as fp:
        for path in input_paths:
            fp.write(path)
    return True


def extract_archive(input_path: str, output_path: str, verbose: bool = VERBOSE_BY_DEFAULT):
    if verbose:
        logger.info("Extracting archive: %s -> %s")

    hodgepodge.files.mkdir(output_path)
    with zipfile.ZipFile(input_path, 'r') as fp:
        fp.extractall(output_path)


def get_file_list(input_path: str) -> List[str]:
    with zipfile.ZipFile(input_path, 'r') as fp:
        return fp.namelist()

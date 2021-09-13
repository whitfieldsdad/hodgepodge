from typing import List
from hodgepodge.constants import VERBOSE_BY_DEFAULT

import hodgepodge.files
import zipfile
import logging


logger = logging.getLogger(__name__)


def extract_archive(input_path: str, output_path: str, verbose: bool = VERBOSE_BY_DEFAULT):
    if verbose:
        logger.info("Extracting archive: %s -> %s")

    hodgepodge.files.mkdir(output_path)
    with zipfile.ZipFile(input_path, 'r') as fp:
        fp.extractall(output_path)


def get_file_list(input_path: str) -> List[str]:
    with zipfile.ZipFile(input_path, 'r') as fp:
        return fp.namelist()

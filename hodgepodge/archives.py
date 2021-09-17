from typing import List

import hodgepodge.files
import zipfile
import logging


logger = logging.getLogger(__name__)


def extract_archive(input_path: str, output_path: str):
    """
    Extract the specified archive to the provided output path.

    :param input_path: the path to the archive.
    :param output_path: the path to extract the archive to.
    """
    hodgepodge.files.mkdir(output_path)
    with zipfile.ZipFile(input_path, 'r') as fp:
        fp.extractall(output_path)


def get_file_list(input_path: str) -> List[str]:
    """
    Return the path of each of the files within the specified archive.

    :param input_path: the path to the archive.
    :return: a list of filenames.
    """
    with zipfile.ZipFile(input_path, 'r') as fp:
        return fp.namelist()

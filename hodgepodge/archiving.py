from typing import Iterable

import hodgepodge.files
import zipfile


def extract_archive(archive_path: str, output_path: str):
    hodgepodge.files.mkdir(output_path)
    with zipfile.ZipFile(archive_path, 'r') as fp:
        fp.extractall(output_path)


def get_archive_filenames(archive_path: str) -> Iterable[str]:
    with zipfile.ZipFile(archive_path, 'r') as fp:
        return fp.namelist()

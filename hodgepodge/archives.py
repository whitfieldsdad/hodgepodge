from typing import List

import hodgepodge.files
import zipfile


def create_archive(input_paths: List[str], output_path: str):
    output_dir = hodgepodge.files.dirname(output_path)
    hodgepodge.files.mkdir(output_dir)

    with zipfile.ZipFile(output_path, 'w') as fp:
        for path in input_paths:
            fp.write(path)


def extract_archive(input_path: str, output_path: str):
    hodgepodge.files.mkdir(output_path)
    with zipfile.ZipFile(input_path, 'r') as fp:
        fp.extractall(output_path)


def get_file_list(input_path: str) -> List[str]:
    with zipfile.ZipFile(input_path, 'r') as fp:
        return fp.namelist()

from typing import Optional
from hodgepodge.constants import INCLUDE_HASHES_BY_DEFAULT
from hodgepodge.hashing import _Hashes

import requests
import shutil
import hodgepodge.files
import hodgepodge.hashing


def download_file(url: str, path: str, session: Optional[requests.Session] = None,
                  include_hashes: bool = INCLUDE_HASHES_BY_DEFAULT) -> Optional[_Hashes]:

    hodgepodge.files.mkdir(path)
    with open(path, 'wb') as fp:
        session = session or requests.Session()
        response = session.get(url)
        response.raise_for_status()

        shutil.copyfileobj(response.raw, fp)
        if include_hashes:
            return hodgepodge.hashing.get_file_hashes(path)

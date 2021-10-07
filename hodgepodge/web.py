from requests import Session
from typing import Optional
from hodgepodge.hashing import Hashes
from hodgepodge.files import INCLUDE_FILE_HASHES_BY_DEFAULT

import hodgepodge.http


def download_file(url: str, path: str, session: Optional[Session] = None,
                  include_file_hashes: bool = INCLUDE_FILE_HASHES_BY_DEFAULT) -> Optional[Hashes]:

    return hodgepodge.http.download_file(
        url=url,
        path=path,
        session=session,
        include_file_hashes=include_file_hashes,
    )

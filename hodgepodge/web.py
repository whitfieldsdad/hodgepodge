from requests import Session
from typing import Optional, Dict
from hodgepodge.constants import INCLUDE_HASHES_BY_DEFAULT, VERBOSE_BY_DEFAULT

import hodgepodge.requests
import logging

logger = logging.getLogger(__name__)


def download_file(url: str, path: str, session: Optional[Session] = None,
                  include_hashes: bool = INCLUDE_HASHES_BY_DEFAULT, verbose: bool = VERBOSE_BY_DEFAULT) -> Optional[Dict[str, str]]:

    return hodgepodge.requests.download_file(
        url=url,
        path=path,
        session=session,
        include_hashes=include_hashes,
        verbose=verbose,
    )

from hodgepodge.constants import INCLUDE_FILE_HASHES_BY_DEFAULT
from dataclasses import dataclass
from typing import Iterable, Optional, Dict
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import hodgepodge.files
import hodgepodge.hashing
import logging
import shutil

logger = logging.getLogger(__name__)

DEFAULT_MAX_RETRIES_ON_CONNECTION_ERRORS = 5
DEFAULT_MAX_RETRIES_ON_READ_ERRORS = 5
DEFAULT_MAX_RETRIES_ON_REDIRECT = 5

DEFAULT_BACKOFF_FACTOR = 0.25
DEFAULT_PREFIXES = ['http://', 'https://']


@dataclass(frozen=True)
class HttpRequestPolicy:
    def to_http_adapter(self) -> HTTPAdapter:
        raise NotImplementedError()


@dataclass(frozen=True)
class AutomaticRetryPolicy(HttpRequestPolicy):
    max_retries_on_connection_errors: int = DEFAULT_MAX_RETRIES_ON_CONNECTION_ERRORS
    max_retries_on_read_errors: int = DEFAULT_MAX_RETRIES_ON_READ_ERRORS
    max_retries_on_redirects: int = DEFAULT_MAX_RETRIES_ON_REDIRECT
    backoff_factor: float = DEFAULT_BACKOFF_FACTOR

    def to_http_adapter(self) -> HTTPAdapter:
        return HTTPAdapter(
            max_retries=Retry(
                connect=self.max_retries_on_connection_errors,
                read=self.max_retries_on_read_errors,
                redirect=self.max_retries_on_redirects,
                backoff_factor=self.backoff_factor
            )
        )


def get_automatic_retry_policy(max_retries_on_connection_errors: int = DEFAULT_MAX_RETRIES_ON_CONNECTION_ERRORS,
                               max_retries_on_read_errors: int = DEFAULT_MAX_RETRIES_ON_READ_ERRORS,
                               max_retries_on_redirects: int = DEFAULT_MAX_RETRIES_ON_REDIRECT,
                               backoff_factor: float = DEFAULT_BACKOFF_FACTOR) -> AutomaticRetryPolicy:
    return AutomaticRetryPolicy(
        max_retries_on_connection_errors=max_retries_on_connection_errors,
        max_retries_on_read_errors=max_retries_on_read_errors,
        max_retries_on_redirects=max_retries_on_redirects,
        backoff_factor=backoff_factor,
    )


def attach_http_request_policies_to_session(session: Session, policies: Iterable[HttpRequestPolicy],
                                            prefixes: Iterable[str] = None):

    adapters = [policy.to_http_adapter() for policy in policies]
    attach_http_adapters_to_session(session=session, adapters=adapters, prefixes=prefixes)


def attach_http_adapters_to_session(session: Session, adapters: Iterable[HTTPAdapter], prefixes: Iterable[str] = None):
    prefixes = prefixes or DEFAULT_PREFIXES
    for prefix in prefixes:
        for adapter in adapters:
            session.mount(prefix, adapter)


def download_file(url: str, path: str, session: Optional[Session] = None,
                  include_file_hashes: bool = INCLUDE_FILE_HASHES_BY_DEFAULT) -> Optional[Dict[str, str]]:

    logging.info("Downloading file_search: {} -> {}".format(url, path))
    hodgepodge.files.mkdir(path)
    with open(path, 'wb') as fp:
        session = session or Session()
        response = session.get(url)
        response.raise_for_status()

        shutil.copyfileobj(response.raw, fp)
        if include_file_hashes:
            return hodgepodge.hashing.get_file_hashes(path)

from typing import Dict
from dataclasses import dataclass
from hodgepodge.constants import FOLLOW_SYMLINKS_BY_DEFAULT, INCLUDE_HASHES_BY_DEFAULT, VERBOSE_BY_DEFAULT
from pathlib import Path

import collections
import hodgepodge.hashing
import os.path
import shutil
import datetime
import logging
import os

logger = logging.getLogger(__name__)

FileTimestamps = collections.namedtuple('Timestamps', ['modify_time', 'access_time', 'change_time'])


@dataclass()
class File:
    seen_time: datetime.datetime
    hashes: Dict[str, str]
    last_access_time: datetime.datetime
    last_change_time: datetime.datetime
    last_modify_time: datetime.datetime
    name: str
    path: str
    real_path: str
    size: int


def get_file_metadata(path: str, follow_symlinks: bool = FOLLOW_SYMLINKS_BY_DEFAULT, include_hashes: bool = INCLUDE_HASHES_BY_DEFAULT, verbose: bool = VERBOSE_BY_DEFAULT) -> File:
    stat_result = os.stat(path, follow_symlinks=follow_symlinks)
    size = stat_result.st_size

    last_modify_time = datetime.datetime.fromtimestamp(stat_result.st_mtime_ns / 1e9)
    last_access_time = datetime.datetime.fromtimestamp(stat_result.st_atime_ns / 1e9)
    last_change_time = datetime.datetime.fromtimestamp(stat_result.st_ctime_ns / 1e9)

    path = get_absolute_path(path)
    name = get_base_name(path)
    real_path = get_real_path(path)

    hashes = None
    if include_hashes:
        hashes = hodgepodge.hashing.get_file_hashes(path, verbose=verbose)

    return File(
        seen_time=datetime.datetime.now(),
        name=name,
        path=path,
        real_path=real_path,
        size=size,
        last_modify_time=last_modify_time,
        last_access_time=last_access_time,
        last_change_time=last_change_time,
        hashes=hashes,
    )


def get_file_timestamps(path: str) -> FileTimestamps:
    st = get_file_stat(path)
    return FileTimestamps(
        modify_time=st.st_mtime,
        access_time=st.st_atime,
        change_time=st.st_ctime,
    )


def get_file_size(path: str) -> int:
    return get_file_stat(path).st_size


def get_file_stat(path: str) -> os.stat_result:
    try:
        return os.stat(path)
    except OSError:
        try:
            return os.lstat(path)
        except OSError:
            raise


def exists(path: str) -> bool:
    path = get_real_path(path)
    return os.path.exists(path)


def delete(*paths: str) -> None:
    for path in paths:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)


def touch(path: str):
    path = get_real_path(path)
    open(path, 'wb').close()


def mkdir(path: str, verbose: bool = VERBOSE_BY_DEFAULT) -> None:
    path = get_real_path(path)
    if path != '/':
        if verbose:
            logger.info("Creating directory: %s", path)
        Path(path).mkdir(parents=True, exist_ok=True)


def dirname(path: str) -> str:
    path = get_real_path(path)
    return os.path.dirname(path)


def get_base_name(path: str) -> str:
    return os.path.basename(path)


def get_absolute_path(path: str) -> str:
    return os.path.abspath(path)


def is_absolute_path(path: str) -> bool:
    return os.path.isabs(path)


def is_relative_path(path: str) -> bool:
    return is_absolute_path(path) is False


def expand_path_variables(path: str) -> str:
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    return path


def get_real_path(path: str) -> str:
    path = expand_path_variables(path)
    return os.path.realpath(path)


def is_regular_file(path: str) -> bool:
    return os.path.isfile(path)


def is_directory(path: str) -> bool:
    return os.path.isdir(path)


def is_symlink(path: str) -> bool:
    return os.path.islink(path)


def is_broken_symlink(path: str) -> bool:
    return is_symlink(path) and os.path.exists(path) is False

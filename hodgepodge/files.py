from hodgepodge.constants import FOLLOW_SYMLINKS_BY_DEFAULT, INCLUDE_FILE_HASHES_BY_DEFAULT
from hodgepodge.objects.host.file import File
from hodgepodge.objects.host.file_stat_result import FileStatResult
from pathlib import Path

import hodgepodge.time
import hodgepodge.hashing
import os.path
import shutil
import datetime
import logging
import stat
import os

from hodgepodge.objects.host.file_timestamps import FileTimestamps

logger = logging.getLogger(__name__)


def get_file_metadata(path: str, follow_symlinks: bool = FOLLOW_SYMLINKS_BY_DEFAULT,
                      include_file_hashes: bool = INCLUDE_FILE_HASHES_BY_DEFAULT) -> File:

    path = get_absolute_path(path)
    real_path = get_real_path(path)
    stat_result = get_file_stat(path, follow_symlinks=follow_symlinks)

    hashes = None
    if include_file_hashes and stat.S_ISREG(stat_result.st_mode):
        hashes = hodgepodge.hashing.get_file_hashes(path)

    return File(
        time=datetime.datetime.now(),
        path=path,
        real_path=real_path,
        hashes=hashes,
        stat_result=stat_result,
    )


def get_file_size(path: str) -> int:
    return get_file_stat(path).st_size


def get_file_stat(path: str, follow_symlinks: bool = FOLLOW_SYMLINKS_BY_DEFAULT) -> FileStatResult:
    st = os.stat(path, follow_symlinks=follow_symlinks)
    return FileStatResult(
        st_mode=st.st_mode,
        st_ino=st.st_ino,
        st_dev=st.st_dev,
        st_nlink=st.st_nlink,
        st_uid=st.st_uid,
        st_gid=st.st_gid,
        st_size=st.st_size,
        st_atime=st.st_atime,
        st_mtime=st.st_mtime,
        st_ctime=st.st_ctime,
    )


def get_file_timestamps(path: str, follow_symlinks: bool = FOLLOW_SYMLINKS_BY_DEFAULT) -> FileTimestamps:
    return get_file_stat(path=path, follow_symlinks=follow_symlinks).timestamps


def exists(path: str) -> bool:
    path = get_real_path(path)
    return os.path.exists(path)


def delete(*paths: str):
    for path in paths:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)


def touch(path: str):
    path = get_real_path(path)
    open(path, 'wb').close()


def mkdir(path: str) -> None:
    path = get_real_path(path)
    if path != '/':
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

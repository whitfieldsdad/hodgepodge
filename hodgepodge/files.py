from hodgepodge.hashing import _Hashes
from pathlib import Path

import collections
import hodgepodge.hashing
import os.path
import shutil

Timestamps = collections.namedtuple('Timestamps', ['modify_time', 'access_time', 'change_time'])


def get_file_timestamps(path: str) -> Timestamps:
    st = get_file_stat(path)
    return Timestamps(
        modify_time=st.st_mtime,
        access_time=st.st_atime,
        change_time=st.st_ctime,
    )


def get_file_size(path: str) -> int:
    return get_file_stat(path).st_size


def get_file_hashes(path: str) -> _Hashes:
    return hodgepodge.hashing.get_file_hashes(path)


def get_file_stat(path: str) -> os.stat_result:
    try:
        return os.stat(path)
    except OSError:
        try:
            return os.lstat(path)
        except OSError:
            raise


def exists(path: str) -> bool:
    return os.path.exists(path)


def delete(*paths: str) -> None:
    for path in paths:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)


def touch(path: str):
    open(path, 'wb').close()


def mkdir(path: str) -> None:
    if path != '/':
        Path(path).mkdir(parents=True, exist_ok=True)


def dirname(path: str) -> str:
    return os.path.dirname(path)


def get_absolute_path(path: str) -> str:
    return os.path.abspath(path)


def is_absolute_path(path: str) -> bool:
    return os.path.isabs(path)


def is_relative_path(path: str) -> bool:
    return is_absolute_path(path) is False


def get_real_path(path: str) -> str:
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.realpath(path)
    return path


def is_regular_file(path: str) -> bool:
    return os.path.isfile(path)


def is_directory(path: str) -> bool:
    return os.path.isdir(path)


def is_symlink(path: str) -> bool:
    return os.path.islink(path)


def is_broken_symlink(path: str) -> bool:
    return is_symlink(path) and os.path.exists(path) is False

from arrow import arrow
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Iterable, List, Iterator, Union, Tuple
from hodgepodge.hashing import Hashes
from hodgepodge.pattern_matching import STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT

import stat as _stat
import hodgepodge.hashing
import hodgepodge.math
import hodgepodge.time
import datetime
import shutil
import glob
import os

FOLLOW_SYMLINKS_BY_DEFAULT = False
FOLLOW_MOUNT_POINTS_BY_DEFAULT = True
INCLUDE_FILE_HASHES_BY_DEFAULT = False


@dataclass(frozen=True)
class MACTimestamps:
    modify_time: datetime.datetime
    access_time: datetime.datetime
    change_time: datetime.datetime

    def __lt__(self, other: Union[str, int, float, datetime.datetime, datetime.date, arrow.Arrow]):
        return all(t < other for t in self)

    def __gt__(self, other: Union[str, int, float, datetime.datetime, datetime.date, arrow.Arrow]):
        return any(t > other for t in self)

    def __iter__(self) -> Iterator[datetime.datetime]:
        for time in self.modify_time, self.access_time, self.change_time:
            yield time


@dataclass(frozen=True)
class StatResult:
    st_mode: int
    st_ino: int
    st_dev: int
    st_nlink: int
    st_uid: int
    st_gid: int
    st_size: int
    st_atime: float
    st_mtime: float
    st_ctime: float

    def get_mac_timestamps(self) -> MACTimestamps:
        return MACTimestamps(
            modify_time=hodgepodge.time.to_datetime(self.st_mtime),
            access_time=hodgepodge.time.to_datetime(self.st_atime),
            change_time=hodgepodge.time.to_datetime(self.st_ctime),
        )


@dataclass()
class File:
    path: str
    real_path: Optional[str]
    size: int
    mac_timestamps: MACTimestamps
    stat_result: Optional[StatResult]
    hashes: Optional[Hashes]


def get_metadata(
        path: str,
        follow_symlinks: bool = FOLLOW_SYMLINKS_BY_DEFAULT,
        include_file_hashes: bool = INCLUDE_FILE_HASHES_BY_DEFAULT) -> File:

    path = get_absolute_path(path)
    real_path = get_real_path(path)
    stat_result = stat(path, follow_symlinks=follow_symlinks)

    hashes = None
    if include_file_hashes and _stat.S_ISREG(stat_result.st_mode):
        hashes = hodgepodge.hashing.get_file_hashes(path)

    modify_time, access_time, change_time = stat_result.get_mac_timestamps()

    return File(
        path=path,
        real_path=real_path,
        hashes=hashes,
        size=stat_result.st_size,
        mac_timestamps=MACTimestamps(
            modify_time=modify_time,
            access_time=access_time,
            change_time=change_time,
        ),
        stat_result=stat_result,
    )


def get_mac_timestamps(path: str, follow_symlinks: bool = FOLLOW_SYMLINKS_BY_DEFAULT):
    st = stat(path, follow_symlinks=follow_symlinks)
    return st.get_mac_timestamps()


def stat(path: str, follow_symlinks: bool = FOLLOW_SYMLINKS_BY_DEFAULT):
    st = os.stat(path, follow_symlinks=follow_symlinks)
    return parse_stat_result(st)


def parse_stat_result(stat_result: os.stat_result) -> StatResult:
    return StatResult(
        st_mode=stat_result.st_mode,
        st_ino=stat_result.st_ino,
        st_dev=stat_result.st_dev,
        st_nlink=stat_result.st_nlink,
        st_uid=stat_result.st_uid,
        st_gid=stat_result.st_gid,
        st_size=stat_result.st_size,
        st_atime=stat_result.st_atime,
        st_mtime=stat_result.st_mtime,
        st_ctime=stat_result.st_ctime,
    )


def get_size(path: str) -> int:
    return stat(path).st_size


class FileSearch:
    def __init__(
            self,
            roots: Optional[List[str]] = None,
            ignored_paths: Optional[List[str]] = None,
            filename_patterns: Optional[List[str]] = None,
            follow_symlinks: Optional[bool] = FOLLOW_SYMLINKS_BY_DEFAULT,
            follow_mount_points: Optional[bool] = FOLLOW_MOUNT_POINTS_BY_DEFAULT,
            case_sensitive: Optional[bool] = STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT,
            min_file_size: Optional[int] = None,
            max_file_size: Optional[int] = None,
            max_search_depth: Optional[int] = None,
            max_search_results: Optional[int] = None,
            include_file_hashes: bool = INCLUDE_FILE_HASHES_BY_DEFAULT):

        self.roots = roots
        self.ignored_paths = ignored_paths
        self.filename_patterns = filename_patterns
        self.follow_symlinks = follow_symlinks
        self.follow_mount_points = follow_mount_points
        self.case_sensitive = case_sensitive
        self.min_file_size = min_file_size
        self.max_file_size = max_file_size
        self.max_search_depth = max_search_depth
        self.max_search_results = max_search_results
        self.include_file_hashes = include_file_hashes

    def iter_matching_files(self) -> Iterator[File]:
        for path, stat_result in self._search():
            path = get_absolute_path(path)
            real_path = get_real_path(path)
            stat_result = stat(path, follow_symlinks=self.follow_symlinks)

            hashes = None
            if self.include_file_hashes and _stat.S_ISREG(stat_result.st_mode):
                hashes = hodgepodge.hashing.get_file_hashes(path)

            modify_time, access_time, change_time = stat_result.get_mac_timestamps()

            yield File(
                path=path,
                real_path=real_path,
                hashes=hashes,
                size=stat_result.st_size,
                mac_timestamps=MACTimestamps(
                    modify_time=modify_time,
                    access_time=access_time,
                    change_time=change_time,
                ),
                stat_result=stat_result,
            )

    def iter_matching_paths(self) -> Iterator[str]:
        for path, _ in self._search():
            yield path

    def _search(self) -> Iterator[Tuple[str, os.stat_result]]:
        roots = get_paths(self.roots)
        ignored_paths = get_paths(self.ignored_paths)

        i = 0
        for root in roots:
            for (path, stat_result) in self._walk(root=root, ignored_paths=ignored_paths):

                #: Filter files by size.
                if (self.min_file_size or self.max_file_size) and not \
                        hodgepodge.math.in_range(stat_result.st_size, minimum=self.min_file_size, maximum=self.max_file_size):
                    continue

                #: Filter files by path/name.
                real_path = get_real_path(path)
                if self.filename_patterns:
                    filenames = {
                        real_path,
                        get_base_name(path),
                        get_base_name(real_path),
                    }
                    if not hodgepodge.pattern_matching.str_matches_glob(filenames, self.filename_patterns, self.case_sensitive):
                        continue

                yield path, stat_result

                #: Optionally limit the number of search results.
                i += 1
                if self.max_search_results and i >= self.max_search_results:
                    return

    def _walk(
            self,
            root: str,
            ignored_paths: Iterable[str],
            current_search_depth: int = 0) -> Iterator[Tuple[str, os.stat_result]]:

        try:
            entries = os.scandir(root)
        except FileNotFoundError:
            return
        except (NotADirectoryError, PermissionError):
            yield root, os.stat(root, follow_symlinks=self.follow_symlinks)
        else:
            yield root, os.stat(root, follow_symlinks=self.follow_symlinks)

            current_search_depth += 1
            for entry in entries:
                path = getattr(entry, 'path')
                stat_result = getattr(entry, 'stat')(follow_symlinks=self.follow_symlinks)
                yield path, stat_result

                #: If this is a subdirectory.
                if _stat.S_ISDIR(stat_result.st_mode):

                    #: Optionally limit search depth.
                    if self.max_search_depth and current_search_depth >= self.max_search_depth:
                        continue

                    #: Optionally disable mount point following.
                    if self.follow_mount_points is False:
                        a = stat_result
                        b = os.stat(root, follow_symlinks=self.follow_symlinks)
                        if a.st_dev != b.st_dev:
                            continue

                    #: Optionally ignore certain directories.
                    if self.ignored_paths and in_directory(path, directories=ignored_paths):
                        continue

                    yield from self._walk(
                        root=path,
                        ignored_paths=ignored_paths,
                        current_search_depth=current_search_depth,
                    )

    def __iter__(self):
        return self.iter_matching_files()


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


def mkdir(path: str):
    path = get_real_path(path)
    if path != '/':
        Path(path).mkdir(parents=True, exist_ok=True)


def dirname(path: str) -> str:
    return os.path.dirname(path)


def expand(path: str) -> str:
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    return path


def get_paths(paths: Iterable[str]) -> List[str]:
    results = set()
    for path in (paths or []):
        path = get_real_path(path)
        if glob.has_magic(path):
            results.update(glob.glob(path))
        else:
            results.add(path)
    return sorted(results)


def in_directory(path: str, directories: Iterable[str]) -> bool:
    path = os.path.join(path, '')
    for directory in directories:
        directory = os.path.join(directory, '')
        if path.startswith(directory):
            return True
    return False


def get_real_path(path: str) -> str:
    path = expand(path)
    return os.path.realpath(path)


def get_base_name(path: str) -> str:
    return os.path.basename(path)


def get_absolute_path(path: str) -> str:
    return os.path.abspath(path)


def is_absolute_path(path: str) -> bool:
    return os.path.isabs(path)


def is_relative_path(path: str) -> bool:
    return is_absolute_path(path) is False


def is_regular_file(path: str) -> bool:
    return os.path.isfile(path)


def is_directory(path: str) -> bool:
    return os.path.isdir(path)


def is_symlink(path: str) -> bool:
    return os.path.islink(path)


def is_broken_symlink(path: str) -> bool:
    return is_symlink(path) and os.path.exists(path) is False

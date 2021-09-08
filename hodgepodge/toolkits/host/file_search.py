from typing import List, Iterator, Optional, Tuple, Dict
from dataclasses import dataclass, field
from hodgepodge.hashing import Hashes
from hodgepodge.constants import FILE_SEARCH_FOLLOW_MOUNTS_BY_DEFAULT, FILE_SEARCH_FOLLOW_SYMLINKS_BY_DEFAULT, \
    DEFAULT_BLOCK_SIZE_FOR_FILE_IO, INCLUDE_HASHES_BY_DEFAULT

import datetime
import dawg
import glob
import hodgepodge.patterns
import hodgepodge.platforms
import hodgepodge.files
import os.path
import os
import stat


@dataclass()
class File:
    hashes: Dict[str, str] = field(repr=False)
    last_access_time: datetime.datetime = field(repr=False)
    last_change_time: datetime.datetime = field(repr=False)
    last_modify_time: datetime.datetime = field(repr=False)
    name: str = field(repr=False)
    path: str
    size: int
    seen_time: datetime.datetime


@dataclass(frozen=True)
class FileSearch:
    roots: List[str]
    excluded_directories: List[str] = None
    filename_glob_patterns: List[str] = None
    follow_mounts: bool = FILE_SEARCH_FOLLOW_MOUNTS_BY_DEFAULT
    follow_symlinks: bool = FILE_SEARCH_FOLLOW_SYMLINKS_BY_DEFAULT
    max_depth: Optional[int] = None
    max_results: Optional[int] = None
    max_file_size: Optional[int] = None
    min_file_size: Optional[int] = None

    def count_files(self) -> int:
        return sum(1 for _ in self.iter_files(include_hashes=False))

    def list_files(self, include_hashes: bool = INCLUDE_HASHES_BY_DEFAULT) -> List[File]:
        return list(self.iter_files(include_hashes=include_hashes))

    def iter_files(self, include_hashes: bool = INCLUDE_HASHES_BY_DEFAULT) -> Iterator[File]:
        files = search(
            roots=self.roots,
            excluded_directories=self.excluded_directories,
            follow_symlinks=self.follow_symlinks,
            follow_mounts=self.follow_mounts,
            filename_glob_patterns=self.filename_glob_patterns,
            min_file_size=self.min_file_size,
            max_file_size=self.max_file_size,
            max_results=self.max_results,
            max_depth=self.max_depth,
            include_hashes=include_hashes,
        )
        for file in files:
            yield file

    def __iter__(self) -> Iterator[File]:
        return self.iter_files()


def search(roots: List[str], excluded_directories: List[str] = None,
           follow_symlinks: bool = FILE_SEARCH_FOLLOW_SYMLINKS_BY_DEFAULT,
           follow_mounts: bool = FILE_SEARCH_FOLLOW_MOUNTS_BY_DEFAULT,
           filename_glob_patterns: List[str] = None,
           min_file_size: Optional[int] = None, max_file_size: Optional[int] = None,
           max_depth: Optional[int] = None, max_results: Optional[int] = None,
           include_hashes: bool = INCLUDE_HASHES_BY_DEFAULT) -> Iterator[File]:

    case_sensitive = False if hodgepodge.platforms.is_windows() else True
    files = walk(
        roots=roots,
        excluded_directories=excluded_directories,
        follow_symlinks=follow_symlinks,
        follow_mounts=follow_mounts,
        max_depth=max_depth,
        max_results=max_results,
        include_hashes=include_hashes,
    )
    results = 0
    for file in files:

        #: Filter files by size.
        if (min_file_size is not None and file.size < min_file_size) or \
                (max_file_size is not None and file.size > max_file_size):
            continue

        #: Filter files by name and path.
        if filename_glob_patterns and not hodgepodge.patterns.any_string_matches_any_glob(
            values=[file.name, file.path],
            patterns=filename_glob_patterns,
            case_sensitive=case_sensitive,
        ):
            continue

        yield file

        #: Optionally limit the number of search results.
        results += 1
        if max_results and results >= max_results:
            return


def walk(roots: List[str], excluded_directories: List[str] = None,
         follow_symlinks: bool = FILE_SEARCH_FOLLOW_SYMLINKS_BY_DEFAULT,
         follow_mounts: bool = FILE_SEARCH_FOLLOW_MOUNTS_BY_DEFAULT, max_depth: Optional[int] = None,
         max_results: Optional[int] = None, include_hashes: bool = INCLUDE_HASHES_BY_DEFAULT,
         block_size_for_file_hashing: int = DEFAULT_BLOCK_SIZE_FOR_FILE_IO) -> Iterator[File]:

    roots, excluded_directories = map(as_non_overlapping_paths, (roots, excluded_directories))
    for root in roots:
        for (path, stat_result) in _walk(
            root=root,
            excluded_directories=excluded_directories,
            follow_symlinks=follow_symlinks,
            follow_mounts=follow_mounts,
            max_depth=max_depth,
            max_results=max_results,
        ):
            #: Optionally hash the contents of the file using a variety of hash algorithms.
            hashes = None
            if include_hashes and stat.S_ISREG(stat_result.st_mode):
                hashes = hodgepodge.hashing.get_file_hashes(path, block_size=block_size_for_file_hashing).get_hex_digests()

            file = File(
                seen_time=datetime.datetime.now(),
                name=os.path.basename(path),
                path=path,
                size=stat_result.st_size,
                last_modify_time=datetime.datetime.fromtimestamp(stat_result.st_mtime_ns / 1e9),
                last_access_time=datetime.datetime.fromtimestamp(stat_result.st_atime_ns / 1e9),
                last_change_time=datetime.datetime.fromtimestamp(stat_result.st_ctime_ns / 1e9),
                hashes=hashes,
            )
            yield file


def _walk(root: str, excluded_directories: List[str], follow_symlinks: bool, follow_mounts: bool,
          max_depth: Optional[int], max_results: Optional[int], depth: int = 0,
          last_stat_result: Optional[os.stat_result] = None) -> Iterator[Tuple[str, os.stat_result]]:
    try:
        entries = os.scandir(root)
    except FileNotFoundError:
        return
    except (NotADirectoryError, PermissionError):
        yield root, os.stat(root, follow_symlinks=follow_symlinks)
    else:
        yield root, os.stat(root, follow_symlinks=follow_symlinks)

        #: For each file in the directory.
        for entry in entries:
            path = entry.path
            stat_result = entry.stat(follow_symlinks=follow_symlinks)
            yield path, stat_result

            #: If this is a directory.
            if stat.S_ISDIR(stat_result.st_mode):

                #: Restrict search depth.
                if max_depth and depth >= max_depth:
                    continue

                #: Restrict search breadth by device.
                if follow_mounts is False and (last_stat_result and stat_result.st_dev != last_stat_result.st_dev):
                    continue

                #: Restrict search breadth by directory.
                if excluded_directories and path_in_any_directory(path, excluded_directories):
                    continue

                yield from _walk(
                    root=path,
                    excluded_directories=excluded_directories,
                    follow_symlinks=follow_symlinks,
                    follow_mounts=follow_mounts,
                    last_stat_result=stat_result,
                    depth=depth + 1,
                    max_depth=max_depth,
                    max_results=max_results,
                )


def path_in_directory(path: str, directory: str) -> bool:
    path = os.path.join(path, '')
    directory = os.path.join(directory, '')
    return path.startswith(directory)


def path_in_any_directory(path: str, directories: List[str]) -> bool:
    for directory in directories:
        if path_in_directory(path, directory):
            return True
    return False


def as_paths(paths: List[str]) -> List[str]:
    results = set()
    for path in paths or []:
        path = hodgepodge.files.get_real_path(path)
        if glob.has_magic(path):
            results.update(set(glob.glob(path)))
        else:
            results.add(path)
    return sorted(results)


def as_non_overlapping_paths(paths) -> List[str]:
    paths = as_paths(paths)
    if len(paths) < 2:
        return paths

    #: Otherwise, construct a directed acyclic word graph (DAWG) containing each path.
    keys_to_paths = dict((os.path.join(path, ''), path) for path in paths)
    graph = dawg.CompletionDAWG(keys_to_paths.keys())

    #: Identify and remove any overlapping paths (e.g. ['/usr/', '/usr/bin/'] to ['/usr/']).
    roots = set()
    for key, path in keys_to_paths.items():
        prefixes = graph.prefixes(key)
        if len(prefixes) == 1:
            roots.add(path)
    return sorted(roots)

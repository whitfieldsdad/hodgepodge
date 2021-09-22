from dataclasses import dataclass
from typing import List, Iterator, Iterable, Optional, Tuple
from hodgepodge.files import File
from hodgepodge.constants import FOLLOW_MOUNT_POINTS_BY_DEFAULT, FOLLOW_SYMLINKS_BY_DEFAULT, \
    INCLUDE_FILE_HASHES_BY_DEFAULT, STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT

import dawg
import glob
import hodgepodge.types
import hodgepodge.patterns
import hodgepodge.platforms
import hodgepodge.hashing
import os.path
import os
import stat


@dataclass(frozen=True)
class FileSearch:
    roots: Optional[List[str]] = None
    ignored_paths: Optional[List[str]] = None
    filename_patterns: Optional[List[str]] = None
    case_sensitive: Optional[bool] = STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT
    min_file_size: Optional[int] = None
    max_file_size: Optional[int] = None
    max_search_depth: Optional[int] = None
    max_search_results: Optional[int] = None
    include_file_hashes: bool = INCLUDE_FILE_HASHES_BY_DEFAULT
    follow_symlinks: bool = FOLLOW_SYMLINKS_BY_DEFAULT
    follow_mount_points: bool = FOLLOW_MOUNT_POINTS_BY_DEFAULT

    def get_matching_files(self) -> List[File]:
        return list(self.iter_matching_files())

    def iter_matching_files(self) -> Iterator[File]:
        files = walk(
            roots=self.roots,
            ignored_paths=self.ignored_paths,
            max_search_depth=self.max_search_depth,
            max_search_results=self.max_search_results,
            include_file_hashes=self.include_file_hashes,
        )
        search_results = 0
        for file in files:

            #: Filter files by file_search size.
            if (self.min_file_size and file.size < self.min_file_size) or \
                    (self.max_file_size and file.size > self.max_file_size):
                continue

            #: Filter files by name and path.
            if self.filename_patterns:
                matches = hodgepodge.patterns.str_matches_glob(
                    values=file.names,
                    patterns=self.filename_patterns,
                    case_sensitive=self.case_sensitive,
                )
                if matches is False:
                    continue

            yield file

            #: Optionally limit the number of search results.
            search_results += 1
            if self.max_search_results and search_results >= self.max_search_results:
                return

    def __iter__(self) -> Iterator[File]:
        return self.iter_matching_files()


def get_matching_files(self) -> List[File]:
    return list(self.iter_matching_files())


def iter_matching_files(
        roots: Optional[List[str]] = None,
        ignored_paths: Optional[List[str]] = None,
        filename_patterns: Optional[List[str]] = None,
        case_sensitive: Optional[bool] = STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT,
        min_file_size: Optional[int] = None,
        max_file_size: Optional[int] = None,
        max_search_depth: Optional[int] = None,
        max_search_results: Optional[int] = None,
        include_file_hashes: bool = INCLUDE_FILE_HASHES_BY_DEFAULT) -> Iterator[File]:

    filename_patterns = set(filename_patterns) if filename_patterns else None

    min_file_size = max(min_file_size, 0) if min_file_size is not None else None
    max_file_size = max(max_file_size, 0) if max_file_size is not None else None

    max_search_results = max(max_search_results, 0) if max_search_results is not None else None
    max_search_depth = max(max_search_depth, 0) if max_search_depth is not None else None

    files = walk(
        roots=roots,
        ignored_paths=ignored_paths,
        max_search_depth=max_search_depth,
        max_search_results=max_search_results,
        include_file_hashes=include_file_hashes,
    )
    results = 0
    for file in files:

        #: Filter files by file_search size.
        if (min_file_size and file.size < min_file_size) or (max_file_size and file.size > max_file_size):
            continue

        #: Filter files by name and path.
        if filename_patterns:
            matches = hodgepodge.patterns.str_matches_glob(
                values=[file.name, file.path],
                patterns=filename_patterns,
                case_sensitive=case_sensitive,
            )
            if matches is False:
                continue

        yield file

        #: Optionally limit the number of search results.
        results += 1
        if max_search_results and results >= max_search_results:
            return


def walk(
        roots: Optional[List[str]] = None,
        ignored_paths: Optional[List[str]] = None,
        follow_symlinks: Optional[bool] = FOLLOW_SYMLINKS_BY_DEFAULT,
        follow_mount_points: Optional[bool] = FOLLOW_MOUNT_POINTS_BY_DEFAULT,
        max_search_depth: Optional[int] = None,
        max_search_results: Optional[int] = None,
        include_file_hashes: bool = INCLUDE_FILE_HASHES_BY_DEFAULT) -> Iterator[File]:

    roots = as_non_overlapping_paths(roots)
    ignored_paths = as_non_overlapping_paths(ignored_paths)

    follow_symlinks = FOLLOW_SYMLINKS_BY_DEFAULT if follow_symlinks is None else follow_symlinks
    follow_mount_points = FOLLOW_MOUNT_POINTS_BY_DEFAULT if follow_mount_points is None else follow_mount_points

    i = 0
    for root in roots:
        for (path, stat_result) in _walk(
            root=root,
            ignored_paths=ignored_paths,
            follow_symlinks=follow_symlinks,
            follow_mount_points=follow_mount_points,
            max_search_depth=max_search_depth,
            current_search_depth=0,
        ):
            yield hodgepodge.files.get_file_metadata(
                path=path,
                include_file_hashes=include_file_hashes,
                follow_symlinks=follow_symlinks,
            )

            i += 1
            if max_search_results and i >= max_search_results:
                break


def _walk(
        root: str,
        ignored_paths: Iterable[str],
        follow_symlinks: bool,
        follow_mount_points: bool,
        max_search_depth: Optional[int],
        current_search_depth: int,
        parent_directory_stat_result: Optional[os.stat_result] = None) -> Iterator[Tuple[str, os.stat_result]]:

    try:
        entries = os.scandir(root)
    except FileNotFoundError:
        return
    except (NotADirectoryError, PermissionError):
        yield root, os.stat(root, follow_symlinks=follow_symlinks)
    else:
        yield root, os.stat(root, follow_symlinks=follow_symlinks)

        current_search_depth += 1
        for entry in entries:
            path = getattr(entry, 'path')
            stat_result = getattr(entry, 'stat')(follow_symlinks=follow_symlinks)
            yield path, stat_result

            #: If this is a directory.
            if stat.S_ISDIR(stat_result.st_mode):

                #: Restrict search depth.
                if max_search_depth and current_search_depth >= max_search_depth:
                    continue

                #: Restrict search breadth by device.
                if follow_mount_points is False and \
                        (parent_directory_stat_result and stat_result.st_dev != parent_directory_stat_result.st_dev):
                    continue

                #: Restrict search breadth by directory.
                if ignored_paths and path_in_any_directory(path, ignored_paths):
                    continue

                yield from _walk(
                    root=path,
                    ignored_paths=ignored_paths,
                    follow_symlinks=follow_symlinks,
                    follow_mount_points=follow_mount_points,
                    parent_directory_stat_result=parent_directory_stat_result,
                    current_search_depth=current_search_depth,
                    max_search_depth=max_search_depth,
                )


def path_in_directory(path: str, directory: str) -> bool:
    path = os.path.join(path, '')
    directory = os.path.join(directory, '')
    return path.startswith(directory)


def path_in_any_directory(path: str, directories: Iterable[str]) -> bool:
    for directory in directories:
        if path_in_directory(path, directory):
            return True
    return False


def resolve_paths(paths: Iterable[str], allow_overlap: bool = True) -> List[str]:
    if allow_overlap:
        return as_paths(paths)
    return as_non_overlapping_paths(paths)


def as_paths(paths: Iterable[str]) -> List[str]:
    results = set()
    for path in (paths or []):
        path = hodgepodge.files.get_real_path(path)
        if glob.has_magic(path):
            results.update(glob.glob(path))
        else:
            results.add(path)
    return list(results)


def as_non_overlapping_paths(paths: Iterable[str]) -> List[str]:
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
    return list(roots)

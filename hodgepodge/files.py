import dataclasses
import fnmatch
import glob
import os
import threading
from typing import Iterable, Iterator, List, Optional, Set, Union
from dataclasses import dataclass
from hodgepodge.hashing import DEFAULT_FILE_HASHING_BLOCK_SIZE, Hash
from hodgepodge import hashing, dataframes
import concurrent.futures

INCLUDE_HASHES = False
INCLUDE_SIZE = False

FOLLOW_SYMLINKS = False


@dataclass()
class File:
    path: str
    name: str
    directory: str
    size: Optional[int] = None
    hashes: List[Hash] = dataclasses.field(default_factory=list)


def get_file_metadata(path: str, include_size: bool = False, include_hashes: bool = False, hash_algorithms: Optional[Iterable[str]] = None, hashing_block_size: int = DEFAULT_FILE_HASHING_BLOCK_SIZE) -> File:
    file = File(
        path=path,
        name=os.path.basename(path),
        directory=os.path.dirname(path),
    )

    if include_size:
        file.size = os.path.getsize(path)
    
    if include_hashes:
        file.hashes = hashing.get_file_hashes(
            path=path,
            algorithms=hash_algorithms,
            block_size=hashing_block_size
        )
    
    return file


def iter_file_metadata(
        roots: Union[str, Iterable[str]], 
        filename_patterns: Optional[Iterable[str]] = None,
        follow_symlinks: bool = FOLLOW_SYMLINKS,
        include_size: bool = INCLUDE_SIZE,
        include_hashes: bool = INCLUDE_HASHES,
        hash_algorithms: Optional[Iterable[str]] = None) -> Iterator[File]:
    
    paths = iter_file_paths(
        roots=roots,
        include_files=True,
        include_directories=False,
        filename_patterns=filename_patterns,
        follow_symlinks=follow_symlinks,
    )

    shutdown_event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for path in paths:
            if shutdown_event.is_set():
                break
    
            future = executor.submit(
                get_file_metadata, 
                path=path, 
                include_size=include_size,
                include_hashes=include_hashes, 
                hash_algorithms=hash_algorithms,
            )
            futures.append(future)
        
        for future in concurrent.futures.as_completed(futures):
            if shutdown_event.is_set():
                break

            yield future.result()


def iter_file_paths(
        roots: Union[str, Iterable[str]], 
        include_files: bool = True,
        include_directories: bool = False,
        filename_patterns: Optional[Iterable[str]] = None,
        follow_symlinks: bool = False) -> Iterator[str]:
    """
    Recursively search for files and directories matching the provided criteria starting from one or more root paths.
    """
    def g(d: str) -> Iterator[str]:
        d = get_real_path(d)
        if "*" in d:
            paths = glob(d)
        else:
            paths = [d]

        for path in paths:
            yield path
            if os.path.isdir(path):
                for directory, _, filenames in os.walk(path, followlinks=follow_symlinks):
                    for filename in filenames:
                        yield os.path.join(directory, filename)

    if not (include_files or include_directories):
        raise ValueError('At least one of include_files or include_directories must be True')

    roots = [roots] if isinstance(roots, str) else roots
    if len(roots) > 1:
        roots = get_non_overlapping_paths(roots)
    
    for root in roots:
        for path in g(root):
            if include_files or include_directories:
                is_dir = os.path.isdir(path)
                if (include_files and is_dir) or (include_directories and not is_dir):
                    continue

            if filename_patterns:
                found = {
                    path,
                    os.path.basename(path),
                }
                if not any(fnmatch.fnmatch(f, pattern) for f in found for pattern in filename_patterns):
                    continue
            
            yield path


def read_documents_from_files(paths: Iterable[str]) -> Iterator[dict]:
    shutdown_event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for path in paths:
            if shutdown_event.is_set():
                break
    
            future = executor.submit(read_documents_from_file, path)
            futures.append(future)
        
        for future in concurrent.futures.as_completed(futures):
            if shutdown_event.is_set():
                break

            yield from future.result()


def read_documents_from_file(path: str) -> Iterator[dict]:
    df = dataframes.read_dataframe(path)
    yield from df.iter_rows(named=True)


def get_non_overlapping_paths(paths: Iterable[str]) -> Set[str]:
    """
    Returns a set of non-overlapping paths from the given iterable of paths.
    
    A path is considered overlapping if it is a subpath of another path in the set.
    """
    paths = sorted(set(paths))
    non_overlapping_paths = set()
    for path in paths:
        if not any(path_overlaps(path, other) for other in non_overlapping_paths):
            non_overlapping_paths.add(path)
    return non_overlapping_paths


def path_overlaps(a: str, b: str, resolve: bool = False) -> bool:
    """
    Checks if path `a` overlaps with path `b`. 
    
    Paths are considered to overlap if one is a subpath of the other. 
    
    For example:

    `/usr/local/bin` overlaps with `/usr/local` as they share a common prefix of `/usr/local`.
    """
    if resolve:
        a = get_real_path(a)
        b = get_real_path(b)

    a = os.path.join(a, '')
    b = os.path.join(b, '')
    return a.startswith(b) or b.startswith(a)


def get_real_path(path: str) -> str:
    """
    Get the real path of `path` by:

    - Expanding environment variables
    - Expanding user home directory
    - Resolving symbolic links
    """
    fs = [ 
        os.path.expandvars,
        os.path.expanduser,
        os.path.realpath,
    ]
    for f in fs:
        path = f(path)
    return path

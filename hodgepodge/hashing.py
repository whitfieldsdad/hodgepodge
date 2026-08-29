from dataclasses import dataclass
import hashlib
from typing import Iterable, Optional
from polars import List

DEFAULT_HASH_ALGORITHMS = [
    'md5',
    'sha1',
    'sha256',
    'blake2s',
    'blake2b',
]

DEFAULT_FILE_HASHING_BLOCK_SIZE = 1024 * 1024


@dataclass()
class Hash:
    algorithm: str
    value: str


def get_file_hashes(path: str, algorithms: Optional[Iterable[str]] = DEFAULT_HASH_ALGORITHMS, block_size: Optional[int] = DEFAULT_FILE_HASHING_BLOCK_SIZE) -> List[Hash]:
    """
    Hash a file using one or more hashing algorithms.
    """
    algorithms = algorithms or DEFAULT_HASH_ALGORITHMS
    hashes = {algo: hashlib.new(algo) for algo in algorithms}
    with open(path, 'rb') as f:
        while chunk := f.read(block_size):
            for o in hashes.values():
                o.update(chunk)
    return [Hash(algorithm=a, value=o.hexdigest()) for a, o in hashes.items()]


def get_hashes(data: bytes, algorithms: Optional[Iterable[str]] = DEFAULT_HASH_ALGORITHMS) -> List[Hash]:
    """
    Hash a bytes object using one or more hashing algorithms.
    """
    hashes = _get_hashers(algorithms)
    for o in hashes.values():
        o.update(data)
    return [Hash(algorithm=a, value=o.hexdigest()) for a, o in hashes.items()]


def _get_hashers(algorithms: Optional[Iterable[str]] = None) -> dict:
    algorithms = algorithms or DEFAULT_HASH_ALGORITHMS
    return {a: hashlib.new(a) for a in algorithms}

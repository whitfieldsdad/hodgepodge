from dataclasses import dataclass
from typing import Dict, Callable, Optional, Union, List
from hodgepodge.constants import DEFAULT_BLOCK_SIZE_FOR_FILE_IO

import hashlib

MD5 = 'md5'
SHA1 = 'sha1'
SHA256 = 'sha256'
SHA512 = 'sha512'

HASH_ALGORITHMS = [MD5, SHA1, SHA256, SHA512]


@dataclass(frozen=True)
class Hash:
    name: str
    value: str


@dataclass(frozen=True)
class Hashes:
    hashes: List[Hash]


@dataclass(frozen=True)
class _Hash:
    name: str
    update: Callable[[bytes], None]
    get_digest: Callable[[], bytes]
    get_hex_digest: Callable[[], str]

    @property
    def digest(self) -> bytes:
        return self.get_digest()

    @property
    def hex_digest(self) -> str:
        return self.get_hex_digest()

    def __bytes__(self):
        return self.digest

    def __str__(self) -> str:
        return self.hex_digest

    def __eq__(self, other: Union[str, bytes]) -> bool:
        a = self
        b = other
        if isinstance(b, str):
            return str(a) == b
        elif isinstance(b, bytes):
            return bytes(a) == b
        elif isinstance(b, _Hash):
            return a.digest == b.digest
        else:
            raise TypeError("Cannot compare '{}' and '{}' ({} and {})".format(type(a).__name__, type(b).__name__, a, b))


@dataclass(frozen=True)
class _Hashes:
    md5: Optional[_Hash] = None
    sha1: Optional[_Hash] = None
    sha256: Optional[_Hash] = None
    sha512: Optional[_Hash] = None

    @property
    def hashes(self):
        hashes = [
            self.md5,
            self.sha1,
            self.sha256,
            self.sha512,
        ]
        return [h for h in hashes if h is not None]

    @property
    def digests(self) -> Dict[str, bytes]:
        return self.get_digests()

    @property
    def hex_digests(self) -> Dict[str, str]:
        return self.get_hex_digests()

    def update(self, data: bytes) -> None:
        for h in self.hashes:
            h.update(data)

    def get_digests(self) -> Dict[str, bytes]:
        return dict((h.name, h.digest) for h in self.hashes)

    def get_hex_digests(self) -> Dict[str, str]:
        return dict((h.name, h.hex_digest) for h in self.hashes)


def _get_hash_via_hashlib(f, data: Optional[bytes] = None) -> _Hash:
    h = _Hash(
        name=f.name,
        update=f.update,
        get_digest=f.digest,
        get_hex_digest=f.hexdigest,
    )
    if data:
        h.update(data)
    return h


def get_md5(data: Optional[bytes] = None) -> _Hash:
    return _get_hash_via_hashlib(hashlib.md5(), data=data)


def get_sha1(data: Optional[bytes] = None) -> _Hash:
    return _get_hash_via_hashlib(hashlib.sha1(), data=data)


def get_sha256(data: Optional[bytes] = None) -> _Hash:
    return _get_hash_via_hashlib(hashlib.sha256(), data=data)


def get_sha512(data: Optional[bytes] = None) -> _Hash:
    return _get_hash_via_hashlib(hashlib.sha512(), data=data)


def get_hashes(data: Optional[bytes] = None) -> _Hashes:
    hashes = _Hashes(
        md5=get_md5(),
        sha1=get_sha1(),
        sha256=get_sha256(),
        sha512=get_sha512(),
    )
    if data:
        hashes.update(data)
    return hashes


def get_file_hashes(path: str, block_size: int = DEFAULT_BLOCK_SIZE_FOR_FILE_IO) -> _Hashes:
    hashes = get_hashes()
    with open(path, 'rb') as fp:
        while True:
            data = fp.read(block_size)
            if not data:
                break
            hashes.update(data)
    return hashes

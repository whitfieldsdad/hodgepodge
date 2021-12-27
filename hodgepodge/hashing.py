from typing import Callable, Optional, Union
from dataclasses import dataclass

import hashlib
import hodgepodge.types
from hodgepodge.serialization import Serializable

DEFAULT_FILE_IO_BLOCK_SIZE = 8192

MD5 = 'md5'
SHA1 = 'sha1'
SHA256 = 'sha256'
SHA512 = 'sha512'

HASH_ALGORITHMS = [MD5, SHA1, SHA256, SHA512]


@dataclass(frozen=True)
class Hashes(Serializable):
    md5: Optional[str]
    sha1: Optional[str]
    sha256: Optional[str]
    sha512: Optional[str]


@dataclass(frozen=True)
class _HashlibWrapper:
    name: str
    update: Callable[[bytes], None]
    get_hex_digest: Callable[[], str]


def _get_hashlib_wrapper(f) -> _HashlibWrapper:
    return _HashlibWrapper(
        name=f.name,
        update=f.update,
        get_hex_digest=f.hexdigest,
    )


def _get_hex_digest_via_hashlib(f, data: Union[str, bytes]) -> str:
    if isinstance(data, str):
        data = hodgepodge.types.str_to_bytes(data)

    h = _get_hashlib_wrapper(f)
    h.update(data)
    return h.get_hex_digest()


def get_md5(data: Union[str, bytes]) -> str:
    return _get_hex_digest_via_hashlib(hashlib.md5(), data=data)


def get_sha1(data: Union[str, bytes]) -> str:
    return _get_hex_digest_via_hashlib(hashlib.sha1(), data=data)


def get_sha256(data: Union[str, bytes]) -> str:
    return _get_hex_digest_via_hashlib(hashlib.sha256(), data=data)


def get_sha512(data: Union[str, bytes]) -> str:
    return _get_hex_digest_via_hashlib(hashlib.sha512(), data=data)


def get_hashes(data: Union[str, bytes]) -> Hashes:
    if isinstance(data, str):
        data = hodgepodge.types.str_to_bytes(data)

    return Hashes(
        md5=get_md5(data),
        sha1=get_sha1(data),
        sha256=get_sha256(data),
        sha512=get_sha512(data),
    )


def get_file_hashes(path: str, block_size: int = DEFAULT_FILE_IO_BLOCK_SIZE) -> Hashes:
    hashes = {
        MD5: _get_hashlib_wrapper(hashlib.md5()),
        SHA1: _get_hashlib_wrapper(hashlib.sha1()),
        SHA256: _get_hashlib_wrapper(hashlib.sha256()),
        SHA512: _get_hashlib_wrapper(hashlib.sha512()),
    }
    with open(path, 'rb') as fp:
        while True:
            data = fp.read(block_size)
            if not data:
                break

            for h in hashes.values():
                h.update(data)

    for (k, h) in hashes.items():
        hashes[k] = h.get_hex_digest()
    return Hashes(**hashes)

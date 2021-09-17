from dataclasses import dataclass
from typing import Dict, Callable
from hodgepodge.constants import DEFAULT_BLOCK_SIZE_FOR_FILE_IO

import logging
import hashlib

logger = logging.getLogger(__name__)

MD5 = 'md5'
SHA1 = 'sha1'
SHA256 = 'sha256'
SHA512 = 'sha512'

HASH_ALGORITHMS = [MD5, SHA1, SHA256, SHA512]


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


def _get_hex_digest_via_hashlib(f, data: bytes) -> str:
    h = _get_hashlib_wrapper(f)
    h.update(data)
    return h.get_hex_digest()


def get_md5(data: bytes) -> str:
    return _get_hex_digest_via_hashlib(hashlib.md5(), data=data)


def get_sha1(data: bytes) -> str:
    return _get_hex_digest_via_hashlib(hashlib.sha1(), data=data)


def get_sha256(data: bytes) -> str:
    return _get_hex_digest_via_hashlib(hashlib.sha256(), data=data)


def get_sha512(data: bytes) -> str:
    return _get_hex_digest_via_hashlib(hashlib.sha512(), data=data)


def get_hashes(data: bytes) -> Dict[str, str]:
    return {
        MD5: get_md5(data),
        SHA1: get_sha1(data),
        SHA256: get_sha256(data),
        SHA512: get_sha512(data),
    }


def get_file_hashes(path: str, block_size: int = DEFAULT_BLOCK_SIZE_FOR_FILE_IO) -> Dict[str, str]:
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
    return hashes

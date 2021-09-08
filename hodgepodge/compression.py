from hodgepodge.exceptions import CompressionError

import hodgepodge.files
import hodgepodge.types
import zlib

GZIP = zlib.MAX_WBITS | 16
AUTO_DETECT_COMPRESSION_TYPE = zlib.MAX_WBITS | 32


def compress(data: bytes) -> bytes:
    return compress_gzip(data)


def decompress(data: bytes) -> bytes:
    return decompress_gzip(data)


def compress_gzip(data: bytes, level: int = 9) -> bytes:
    return _compress(data, level=level, wbits=GZIP)


def decompress_gzip(data: bytes) -> bytes:
    return _decompress(data, wbits=AUTO_DETECT_COMPRESSION_TYPE)


def _compress(data: bytes, level: int = 9, method: int = zlib.DEFLATED, wbits: int = GZIP) -> bytes:
    if isinstance(data, str):
        data = hodgepodge.types.str_to_bytes(data)

    compressor = zlib.compressobj(level, method, wbits)
    try:
        return compressor.compress(data) + compressor.flush()
    except zlib.error as e:
        raise CompressionError("Compression failed") from e


def _decompress(data: bytes, wbits: int = AUTO_DETECT_COMPRESSION_TYPE) -> bytes:
    try:
        return zlib.decompress(data, wbits=wbits)
    except zlib.error as e:
        raise CompressionError("Decompression failed") from e

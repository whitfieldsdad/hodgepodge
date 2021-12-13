import hodgepodge.types
import hodgepodge.compression
import unittest


class CompressionTestCases(unittest.TestCase):
    def test_compress_gzip(self):
        data = b'hello world'
        expected = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\x13\xcbH\xcd\xc9\xc9W(\xcf/\xcaI\x01\x00\x85\x11J\r\x0b\x00\x00\x00'
        result = hodgepodge.compression.compress_gzip(data)
        self.assertEqual(expected, result)

    def test_decompress_gzip(self):
        data = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\x13\xcbH\xcd\xc9\xc9W(\xcf/\xcaI\x01\x00\x85\x11J\r\x0b\x00\x00\x00'
        expected = b'hello world'
        result = hodgepodge.compression.decompress_gzip(data)
        self.assertEqual(expected, result)

import hodgepodge.compression
import unittest


class CompressionTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = b"Hello World"
        cls.gzip_compressed = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\x03\xf3H\xcd\xc9\xc9W\x08\xcf/\xcaI\x01\x00V\xb1\x17J\x0b\x00\x00\x00'

    def test_compress_gzip(self):
        expected = self.gzip_compressed
        result = hodgepodge.compression.compress_gzip(data=self.data)
        self.assertEqual(expected, result)

    def test_decompress_gzip(self):
        expected = self.data
        result = hodgepodge.compression.decompress_gzip(self.gzip_compressed)
        self.assertEqual(expected, result)

from unittest import TestCase
from hodgepodge.hashing import MD5, SHA1, SHA256, SHA512

import hodgepodge.types
import hodgepodge.hashing
import hodgepodge.files
import tempfile
import os


class HashingTestCases(TestCase):
    tmp = None

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.txt = txt = b'hello world'
        cls.tmp = tempfile.mktemp()
        with open(cls.tmp, 'wb') as fp:
            fp.write(txt)
            fp.flush()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.tmp):
            os.unlink(cls.tmp)

    def test_get_hashes(self):
        expected = {
            MD5: '5eb63bbbe01eeed093cb22bb8f5acdc3',
            SHA1: '2aae6c35c94fcfb415dbe95f408b9ce91ee846ed',
            SHA256: 'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9',
            SHA512: '309ecc489c12d6eb4cc40f50c902f2b4d0ed77ee511a7c7a9bcd3ca86d4cd86f989dd35bc5ff499670da34255b45b0cfd830e81f605dcf7dc5542e93ae9cd76f',
        }
        result = hodgepodge.hashing.get_hashes(self.txt)
        self.assertEqual(expected, result)

    def test_get_file_hashes(self):
        expected = {
            MD5: '5eb63bbbe01eeed093cb22bb8f5acdc3',
            SHA1: '2aae6c35c94fcfb415dbe95f408b9ce91ee846ed',
            SHA256: 'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9',
            SHA512: '309ecc489c12d6eb4cc40f50c902f2b4d0ed77ee511a7c7a9bcd3ca86d4cd86f989dd35bc5ff499670da34255b45b0cfd830e81f605dcf7dc5542e93ae9cd76f',
        }
        result = hodgepodge.hashing.get_file_hashes(self.tmp)
        self.assertEqual(expected, result)

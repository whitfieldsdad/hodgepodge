import os
from unittest import TestCase
from hodgepodge import hashing

import tempfile


class HashingTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file_path = tempfile.NamedTemporaryFile(delete=False).name
        with open(cls.test_file_path, 'wb') as f:
            f.write(b"Hello, world!")
            f.flush()
    
    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_file_path)

    def test_get_hashes(self):
        msg = b"Hello, world!"
        hashes = hashing.get_hashes(msg)
        
        self.assertIsInstance(hashes, list)
        self.assertGreater(len(hashes), 0)

        for hash in hashes:
            self.assertIsInstance(hash, hashing.Hash)
            self.assertIn(hash.algorithm, hashing.DEFAULT_HASH_ALGORITHMS)
            self.assertIsInstance(hash.value, str)
            self.assertGreater(len(hash.value), 0)

    def test_get_file_hashes(self):
        hashes = hashing.get_file_hashes(self.test_file_path)
        
        self.assertIsInstance(hashes, list)
        self.assertGreater(len(hashes), 0)

        for hash in hashes:
            self.assertIsInstance(hash, hashing.Hash)
            self.assertIn(hash.algorithm, hashing.DEFAULT_HASH_ALGORITHMS)
            self.assertIsInstance(hash.value, str)
            self.assertGreater(len(hash.value), 0)

    def test_get_file_hashes_returns_same_hashes_as_get_hashes(self):
        with open(self.test_file_path, 'rb') as f:
            file_data = f.read()

        file_hashes = hashing.get_file_hashes(self.test_file_path)
        data_hashes = hashing.get_hashes(file_data)

        self.assertEqual(len(file_hashes), len(data_hashes))

        for file_hash, data_hash in zip(file_hashes, data_hashes):
            self.assertEqual(file_hash.algorithm, data_hash.algorithm)
            self.assertEqual(file_hash.value, data_hash.value)

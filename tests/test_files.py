from unittest import TestCase
from hodgepodge import files, dataframes

import polars as pl
import shutil
import tempfile
import os


class TestFiles(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()

        cls.file_a_path = os.path.join(cls.tempdir, 'a.txt')
        with open(cls.file_a_path, 'w') as f:
            f.write("Hello, World!")
        
        cls.subdir_path = os.path.join(cls.tempdir, 'subdir')
        os.makedirs(cls.subdir_path, exist_ok=True)
    
        cls.file_b_path = os.path.join(cls.subdir_path, 'b.txt')
        with open(cls.file_b_path, 'w') as f:
            f.write("Goodbye, World!")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tempdir)

    def test_iter_file_paths(self):
        expected = [
            self.file_a_path,
            self.file_b_path,
        ]
        result = list(files.iter_file_paths(self.tempdir, include_files=True, include_directories=False))
        self.assertEqual(set(expected), set(result))

    def test_get_file_metadata(self):
        result = files.get_file_metadata(
            self.file_a_path, 
            include_size=True, 
            include_hashes=True,
        )
        self.assertEqual(result.path, self.file_a_path)
        self.assertEqual(result.name, 'a.txt')
        self.assertIsNotNone(result.size)
        self.assertIsNotNone(result.hashes)

    def test_get_non_overlapping_paths(self):
        examples = {
            ('/var', '/var/log'): ['/var'],
            ('/var/log', '/var/log/data-source/log.txt'): ['/var/log'],
            ('/etc', '/var/log'): ['/etc', '/var/log'],
        }
        for (a, b), expected in examples.items():
            with self.subTest(a=a, b=b):
                result = files.get_non_overlapping_paths([a, b])
                self.assertEqual(set(expected), set(result))

    def test_path_overlaps(self):
        examples = {
            ('/var', '/var/log'): True,
            ('/var/log', '/var/log/data-source/log.txt'): True,
            ('/etc', '/var/log'): False,
        }
        for (a, b), expected in examples.items():
            with self.subTest(a=a, b=b):
                result = files.path_overlaps(a, b)
                self.assertEqual(result, expected)

    def test_get_real_path_expands_tilde(self):
        home = '~'
        expected = os.path.expanduser(home)
        result = files.get_real_path(home)
        self.assertEqual(result, expected)

    def test_read_documents_from_file(self):
        rows = [
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': 25},
        ]
        for suffix in ['.csv', '.csv.gz', '.json', '.json.gz', '.jsonl', '.jsonl.gz', '.parquet', '.yaml']:
            with self.subTest(suffix=suffix):
                with tempfile.NamedTemporaryFile(mode='w+', suffix=suffix, delete=True) as temp_file:
                    dataframes.write_dataframe(pl.DataFrame(rows), temp_file.name)
                    try:
                        result = list(files.read_documents_from_file(temp_file.name))
                        self.assertEqual(rows, result)
                    finally:
                        os.remove(temp_file.name)

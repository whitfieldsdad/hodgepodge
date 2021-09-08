from unittest import TestCase
from hodgepodge.toolkits.host.file_search import FileSearch

import hodgepodge.files
import tempfile
import uuid
import os.path
import os


class FileSearchTestCase(TestCase):
    tmp_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        hodgepodge.files.delete(cls.tmp_dir)

    def test_find_with_max_results(self):
        tmp_dir = tempfile.mkdtemp(dir=self.tmp_dir)

        limit = 5
        for i in range(0, limit):
            _, _ = tempfile.mkstemp(dir=tmp_dir)

        results = list(FileSearch(roots=[tmp_dir], max_results=limit - 1))
        self.assertEqual(limit - 1, len(results))

    def test_find_with_min_size(self):
        sz = 128
        _, tmp = tempfile.mkstemp(dir=self.tmp_dir)
        with open(tmp, 'wb') as fp:
            fp.write(os.urandom(sz))

        a = [f.path for f in FileSearch(roots=[tmp], min_file_size=sz)]
        self.assertIn(tmp, a)

        b = [f.path for f in FileSearch(roots=[tmp], min_file_size=sz + 1)]
        self.assertNotIn(tmp, b)

    def test_find_with_max_size(self):
        sz = 128
        _, tmp = tempfile.mkstemp(dir=self.tmp_dir)
        with open(tmp, 'wb') as fp:
            fp.write(os.urandom(sz))

        a = [f.path for f in FileSearch(roots=[tmp], max_file_size=sz)]
        self.assertIn(tmp, a)

        b = [f.path for f in FileSearch(roots=[tmp], max_file_size=sz - 1)]
        self.assertNotIn(tmp, b)

    def test_find_with_absolute_paths(self):
        _, tmp = tempfile.mkstemp(dir=self.tmp_dir)

        paths = [f.path for f in FileSearch(roots=[tmp])]
        self.assertTrue(all(hodgepodge.files.is_absolute_path(path) for path in paths))

    def test_find_with_relative_paths(self):
        _, tmp = tempfile.mkstemp(dir=self.tmp_dir)

        paths = [f.path for f in FileSearch(roots=[os.path.relpath(os.getcwd(), tmp)])]
        self.assertTrue(all(hodgepodge.files.is_relative_path(path) for path in paths))

    def test_find_regular_file(self):
        _, tmp = tempfile.mkstemp(dir=self.tmp_dir)

        expected = [tmp]
        result = [f.path for f in FileSearch(roots=[tmp])]
        self.assertEqual(expected, result)

    def test_find_directory(self):
        tmp_dir = tempfile.mkdtemp(dir=self.tmp_dir)
        _, tmp = tempfile.mkstemp(dir=tmp_dir)

        expected = {
            tmp_dir,
            tmp,
        }
        result = {f.path for f in FileSearch(roots=[tmp_dir])}
        self.assertEqual(expected, result)

    def test_find_non_existent_file(self):
        path = uuid.uuid4().hex
        self.assertFalse(hodgepodge.files.exists(path))

        result = list(FileSearch(roots=[path]))
        self.assertEqual([], result)

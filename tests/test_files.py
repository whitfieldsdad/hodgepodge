from unittest import TestCase
from hodgepodge.files import FileSearch, File, MACTimestamps, StatResult

import hodgepodge.files
import tempfile
import uuid
import os


class FileTestCases(TestCase):
    tmp_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        hodgepodge.files.delete(cls.tmp_dir)

    def test_get_mac_timestamps(self):
        with tempfile.NamedTemporaryFile(dir=self.tmp_dir) as tmp:
            timestamps = hodgepodge.files.get_mac_timestamps(path=tmp.name)
            self.assertIsInstance(timestamps, MACTimestamps)

    def test_get_metadata(self):
        with tempfile.NamedTemporaryFile(dir=self.tmp_dir) as tmp:
            metadata = hodgepodge.files.get_metadata(path=tmp.name)
            self.assertIsInstance(metadata, File)

    def test_get_size(self):
        with tempfile.NamedTemporaryFile(dir=self.tmp_dir) as tmp:

            #: The file_search should be zero bytes in size.
            a = hodgepodge.files.get_size(path=tmp.name)
            self.assertEqual(a, 0)

            #: Write 5 bytes to the file_search.
            tmp.write(b"hello")
            tmp.flush()

            #: Verify that the file_search size is now 5.
            b = hodgepodge.files.get_size(tmp.name)
            self.assertEqual(b, 5)

    def test_stat(self):
        with tempfile.NamedTemporaryFile(dir=self.tmp_dir) as tmp:
            st = hodgepodge.files.stat(tmp.name)
            self.assertIsInstance(st, StatResult)

    def test_exists(self):
        tmp = tempfile.mktemp(dir=self.tmp_dir)
        self.assertFalse(hodgepodge.files.exists(tmp))
        hodgepodge.files.touch(tmp)
        self.assertTrue(hodgepodge.files.exists(tmp))

    def test_mkdir(self):
        tmp_dir = tempfile.mktemp(dir=self.tmp_dir)
        self.assertFalse(hodgepodge.files.exists(tmp_dir))

        hodgepodge.files.mkdir(tmp_dir)
        self.assertTrue(hodgepodge.files.exists(tmp_dir))

    def test_dirname(self):
        a = tempfile.mktemp(dir=self.tmp_dir)
        b = tempfile.mktemp(dir=a)
        self.assertEqual(a, hodgepodge.files.dirname(b))

    def test_get_real_path(self):
        for i, (path, expected) in enumerate([
            ('.', os.getcwd()),
            (os.getcwd(), os.getcwd()),
        ]):
            with self.subTest(i=i, path=path):
                result = hodgepodge.files.get_real_path(path)
                self.assertEqual(expected, result)

    def test_is_regular_file(self):
        _, tmp = tempfile.mkstemp(dir=self.tmp_dir)
        self.assertTrue(hodgepodge.files.is_regular_file(tmp))

        tmp_dir = tempfile.mkdtemp(dir=self.tmp_dir)
        self.assertFalse(hodgepodge.files.is_regular_file(tmp_dir))

    def test_is_directory(self):
        _, tmp = tempfile.mkstemp(dir=self.tmp_dir)
        self.assertFalse(hodgepodge.files.is_directory(tmp))

        tmp_dir = tempfile.mkdtemp(dir=self.tmp_dir)
        self.assertTrue(hodgepodge.files.is_directory(tmp_dir))

    def test_is_symlink(self):
        _, a = tempfile.mkstemp()
        b = tempfile.mktemp()
        os.symlink(a, b)

        self.assertTrue(hodgepodge.files.is_symlink(b))
        hodgepodge.files.delete(a, b)
        self.assertFalse(hodgepodge.files.is_symlink(b))

    def test_is_broken_symlink(self):
        _, a = tempfile.mkstemp()
        b = tempfile.mktemp()
        os.symlink(a, b)

        hodgepodge.files.delete(a)
        self.assertTrue(hodgepodge.files.is_symlink(b))
        self.assertTrue(hodgepodge.files.is_broken_symlink(b))
        hodgepodge.files.delete(b)

    def test_get_paths(self):
        home = '$HOME'
        real_home = hodgepodge.files.get_real_path(home)

        for paths, expected in (
            ([home], [real_home]),
            ([real_home], [real_home]),
            ([home, real_home], [real_home])
        ):
            result = hodgepodge.files.get_paths(paths)
            self.assertSetEqual(set(expected), set(result))

    def test_search_with_max_search_results(self):
        tmp_dir = tempfile.mkdtemp(dir=self.tmp_dir)

        limit = 5
        for i in range(0, limit):
            _, _ = tempfile.mkstemp(dir=tmp_dir)

        results = {f.path for f in FileSearch(roots=[tmp_dir], max_search_results=limit - 1)}
        self.assertEqual(limit - 1, len(results))

    def test_search_with_min_file_size(self):
        sz = 128
        _, tmp = tempfile.mkstemp(dir=self.tmp_dir)
        tmp = hodgepodge.files.get_real_path(tmp)
        with open(tmp, 'wb') as fp:
            fp.write(os.urandom(sz))

        a = {f.path for f in FileSearch(roots=[tmp], min_file_size=sz)}
        self.assertIn(tmp, a)

        b = {f.path for f in FileSearch(roots=[tmp], min_file_size=sz + 1)}
        self.assertNotIn(tmp, b)

    def test_search_with_max_file_size(self):
        sz = 128
        _, tmp = tempfile.mkstemp(dir=self.tmp_dir)
        tmp = hodgepodge.files.get_real_path(tmp)
        with open(tmp, 'wb') as fp:
            fp.write(os.urandom(sz))

        a = {f.path for f in FileSearch(roots=[tmp], max_file_size=sz)}
        self.assertIn(tmp, a)

        b = {f.path for f in FileSearch(roots=[tmp], max_file_size=sz - 1)}
        self.assertNotIn(tmp, b)

    def test_search_with_absolute_paths(self):
        _, tmp = tempfile.mkstemp(dir=self.tmp_dir)

        paths = {f.path for f in FileSearch(roots=[tmp])}
        self.assertTrue(all(hodgepodge.files.is_absolute_path(path) for path in paths))

    def test_search_with_regular_file(self):
        _, tmp = tempfile.mkstemp(dir=self.tmp_dir)
        tmp = hodgepodge.files.get_real_path(tmp)

        expected = {tmp}
        result = {f.path for f in FileSearch(roots=[tmp])}
        self.assertEqual(expected, result)

    def test_search_with_directory(self):
        tmp_dir = tempfile.mkdtemp(dir=self.tmp_dir)
        _, tmp = tempfile.mkstemp(dir=tmp_dir)

        tmp, tmp_dir = map(hodgepodge.files.get_real_path, (tmp, tmp_dir))

        expected = {
            tmp_dir,
            tmp,
        }
        result = {f.path for f in FileSearch(roots=[tmp_dir])}
        self.assertEqual(expected, result)

    def test_search_with_non_existent_file(self):
        path = uuid.uuid4().hex
        self.assertFalse(hodgepodge.files.exists(path))

        result = {f.path for f in FileSearch(roots=[path])}
        self.assertEqual(0, len(result))

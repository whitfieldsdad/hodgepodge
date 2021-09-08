from unittest import TestCase
from hodgepodge.files import Timestamps

import hodgepodge.files
import tempfile
import os


class FileTestCases(TestCase):
    tmp_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        hodgepodge.files.delete(cls.tmp_dir)

    def test_get_file_timestamps(self):
        with tempfile.NamedTemporaryFile(dir=self.tmp_dir) as tmp:
            timestamps = hodgepodge.files.get_file_timestamps(path=tmp.name)
            self.assertIsInstance(timestamps, Timestamps)

    def test_get_file_size(self):
        with tempfile.NamedTemporaryFile(dir=self.tmp_dir) as tmp:

            #: The file should be zero bytes in size.
            a = hodgepodge.files.get_file_size(path=tmp.name)
            self.assertEqual(a, 0)

            #: Write 5 bytes to the file.
            tmp.write(b"hello")
            tmp.flush()

            #: Verify that the file size is now 5.
            b = hodgepodge.files.get_file_size(tmp.name)
            self.assertEqual(b, 5)

    def test_get_file_stat(self):
        with tempfile.NamedTemporaryFile(dir=self.tmp_dir) as tmp:
            st = hodgepodge.files.get_file_stat(tmp.name)
            self.assertIsInstance(st, os.stat_result)

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
            #(hodgepodge.files.get_real_path('~'), hodgepodge.files.get_real_path('$HOME')),
            #(hodgepodge.files.get_real_path('$HOME'), hodgepodge.files.get_real_path('~')),
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

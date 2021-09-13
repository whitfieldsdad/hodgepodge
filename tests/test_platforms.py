from unittest import TestCase
from hodgepodge.platforms import WINDOWS, LINUX, DARWIN

import hodgepodge.platforms


class PlatformTestCases(TestCase):
    def test_normalize_os_type(self):
        for os_type, expected in [
            ('darwin', DARWIN),
            ('macOS', DARWIN),
            ('macos', DARWIN),
            ('mac os', DARWIN),
            ('mac os x', DARWIN),
            ('os x', DARWIN),
            ('osx', DARWIN),
            ('linux', LINUX),
            ('ubuntu', LINUX),
            ('centos', LINUX),
            ('debian', LINUX),
            ('rhel', LINUX),
            ('redhat', LINUX),
            ('red hat', LINUX),
            ('windows', WINDOWS),
            ('windows xp', WINDOWS),
            ('MS-DOS', WINDOWS),
            ('DOS', WINDOWS),
            ('cygwin', WINDOWS),
            ('Cygwin 2.2 64 bit (Windows 10 64-bit)', WINDOWS),
        ]:
            with self.subTest(os_type=os_type, expected=expected):
                result = hodgepodge.platforms.normalize_os_type(os_type)
                self.assertEqual(expected, result)

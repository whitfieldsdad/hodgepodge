from unittest import TestCase

import hodgepodge.networking


class NetworkTestCases(TestCase):
    def test_parse_mac_address(self):
        for mac_address, expected in (
            ('00-23-3a-99-0c-21', '00:23:3a:99:0c:21'),
            ('00233a990c21', '00:23:3a:99:0c:21'),
            ('00:23:3A:99:0C:21', '00:23:3a:99:0c:21'),
        ):
            with self.subTest(mac_address=mac_address, expected=expected):
                result = hodgepodge.networking.parse_mac_address(mac_address)
                self.assertEqual(expected, result)

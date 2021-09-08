from unittest import TestCase

import hodgepodge.uuid


class UuidTestCase(TestCase):
    def test_new(self):
        result = hodgepodge.uuid.new()
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 36)

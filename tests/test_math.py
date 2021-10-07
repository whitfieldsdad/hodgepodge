from unittest import TestCase

import hodgepodge.math


class MathTestCases(TestCase):
    def test_in_range(self):
        for value, minimum, maximum, expected in (
            (0, 0, 0, True),
            (25, 25, 25, True),
            (25, 25, None, True),
            (25, None, 25, True),
            (25, 26, None, False),
            (25, 26, 27, False),
        ):
            with self.subTest(value=value, minimum=minimum, maximum=maximum):
                result = hodgepodge.math.in_range(value=value, minimum=minimum, maximum=maximum)
                self.assertEqual(expected, result)

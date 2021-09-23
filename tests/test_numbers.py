from unittest import TestCase

import hodgepodge.numbers


class NumberHelperTestCases(TestCase):
    def test_is_within_range(self):
        for value, minimum, maximum, expected in (
            (0, 0, 0, True),
            (25, 25, 25, True),
            (25, 25, None, True),
            (25, None, 25, True),
            (25, 26, None, False),
            (25, 26, 27, False),
        ):
            with self.subTest(value=value, minimum=minimum, maximum=maximum):
                result = hodgepodge.numbers.is_within_range(value=value, minimum=minimum, maximum=maximum)
                self.assertEqual(expected, result)

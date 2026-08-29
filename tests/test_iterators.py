from unittest import TestCase

from hodgepodge import iterators


class IteratorTestCases(TestCase):
    def test_iter_pairwise(self):
        tests = {
            (1,): [(1, None)],
            (1, 2): [(1, 2)],
            (1, 2, 3): [(1, 2), (2, 3)],
        }
        for input_data, expected in tests.items():
            with self.subTest(input_data=input_data):
                result = list(iterators.iter_pairwise(input_data))
                self.assertEqual(expected, result)

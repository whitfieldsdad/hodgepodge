from unittest import TestCase
from hodgepodge import times

import datetime


class TestTimes(TestCase):
    def test_parse_date(self):
        example_date = '2026-01-01'
        
        expected = datetime.date(2026, 1, 1)
        result = times.parse_date(example_date)

        self.assertIsInstance(result, datetime.date)
        self.assertEqual(result, expected)

    def test_parse_datetime(self):
        inputs = [
            '2026-07-31T19:37:24.384904',
            '2026-07-31T19:37:24',
            '2026-07-31',
            1785541186,
            1785541182.4866266,
            datetime.date(2026, 7, 31),
            datetime.datetime(2026, 7, 31, 19, 37, 24, 384904),
        ]
        for example in inputs:
            with self.subTest(example=example):
                result = times.parse_datetime(example)
                self.assertIsInstance(result, datetime.datetime)

    def test_iter_dates(self):
        a = '2026-01-01'
        b = '2026-01-03'
        expected = [
            '2026-01-01',
            '2026-01-02',
            '2026-01-03',
        ]
        result = [d.isoformat() for d in times.iter_dates(a, b)]
        self.assertEqual(expected, result)

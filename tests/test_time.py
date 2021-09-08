from unittest import TestCase
from hodgepodge.time import Time

import hodgepodge.time
import arrow


class TimeTestCase(TestCase):
    def test_as_epoch_timestamp(self):
        expected = 1436978073.0
        for hint, timestamp in [
            ['float', expected],
            ['int', int(expected)],
            ['arrow', arrow.get(expected)],
            ['datetime.datetime', arrow.get(expected).datetime],
            ['iso-8601', arrow.get(expected).isoformat()],
        ]:
            with self.subTest(hint=hint, timestamp=timestamp):
                result = hodgepodge.time.as_epoch_timestamp(timestamp)
                self.assertEqual(expected, result)

    def test_as_duration(self):
        epoch = arrow.get(0).timestamp()
        timestamp = 1436978073.0

        for hint, duration in [
            ['float', timestamp - epoch],
            ['int', int(timestamp - epoch)],
            ['datetime.timedelta', arrow.get(timestamp) - arrow.get(epoch)],
        ]:
            with self.subTest(hint=hint, timestamp=timestamp):
                expected = Time(
                    years=45,
                    days=206,
                    hours=16,
                    minutes=34,
                    seconds=33,
                )
                result = hodgepodge.time.as_duration(duration)
                self.assertEqual(expected, result)

    def test_within_range(self):
        t = arrow.now()
        a = t.shift(hours=-1).float_timestamp
        b = t.shift(hours=+1).float_timestamp
        t = t.float_timestamp

        subtests = [
            [None, None, True],
            [a, None, True],
            [b, None, False],
            [a, b, True],
            [b, None, False],
            [None, a, False],
            [b, a, False],
        ]
        for i, subtest in enumerate(subtests):
            a, b, expected = subtest

            with self.subTest(i=i, t=t, a=a, b=b):
                result = hodgepodge.time.is_within_range(t, a, b)
                self.assertIsInstance(result, bool)
                self.assertEqual(result, expected)

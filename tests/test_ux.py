from unittest import TestCase

import hodgepodge.ux
import arrow
import time
import re


class UXTestCases(TestCase):
    def test_pluralize(self):
        expected = 'jigglypuffs'
        for string in [
            'jigglypuff',
            'jigglypuffs'
        ]:
            with self.subTest(string=string):
                result = hodgepodge.ux.pluralize(expected)
                self.assertEqual(expected, result)

    def test_remove_suffix(self):
        expected = 'jigglypuff'
        for string in [
            'jigglypuff',
            'jigglypuffs'
        ]:
            with self.subTest(string=string):
                result = hodgepodge.ux.remove_suffix(expected, "s")
                self.assertEqual(expected, result)

    def test_pretty_file_size(self):
        for size, expected in [
            (1000, '1.0KiB'),
            (1000 * 1.5, '1.5KiB'),
            (1000 * 1000 * 1.5, '1.5MiB'),
            (1000 * 1000000, '1.0GiB'),
            (1000 * 1000000 * 1.5, '1.5GiB'),
            (1000 * 1000000000, '1.0TiB'),
            (1000 * 1000000000 * 1.5, '1.5TiB'),
            (1000 * 1000000000000 * 2.7, '2.7PiB'),
            (1000 * 1000000000000000 * 5.4, '5.4EiB'),
            (1000 * 1000000000000000000 * 3, '3.0ZiB'),
        ]:
            with self.subTest(size):
                result = hodgepodge.ux.pretty_file_size(size)
                self.assertEqual(expected, result)

    def test_pretty_time(self):
        for timestamp in [
            1624089237.688544,
            1624089237,
        ]:
            with self.subTest(timestamp=timestamp):
                expected = 'Jun 19, 2021, 07:53:57 AM'
                result = hodgepodge.ux.pretty_time(timestamp, include_delta=False)
                self.assertEqual(expected, result)

    def test_pretty_time_with_delta(self):
        now = time.time()
        for timestamp, expected_parts, expected_tense in [
            [now - 86400, '1 day', 'ago'],
            [now - (86400 * 3), '3 days', 'ago'],
            [now - (86400 * 1.5), '1 day and 12 hours', 'ago'],
            [now - (86400 * 1.45), '1 day, 10 hours, and 48 minutes', 'ago'],
            [now - (86400 * 7), '7 days', 'ago'],
            [now - (86400 * 365), '1 year', 'ago'],
            [now - (86400 * 400), '1 year and 35 days', 'ago'],
            [now - (86400 * 365 * 1.13), '1 year, 47 days, 10 hours, and 48 minutes', 'ago'],
        ]:
            with self.subTest(expected_parts=expected_parts, expected_tense=expected_tense):
                result = hodgepodge.ux.pretty_time(timestamp, include_delta=True)

                #: Parse the delta.
                match = re.match(r'.+\((.*)(ago|from now)\)', result)
                parts, tense = match.groups()
                parts = parts.rstrip()

                self.assertEqual(expected_parts, parts)
                self.assertEqual(expected_tense, tense)

    def test_pretty_duration(self):
        t = arrow.now()
        d = t.shift(days=+30) - t

        result = hodgepodge.ux.pretty_duration(d)
        expected = '30 days'
        self.assertEqual(expected, result)

    def test_join_with_oxford_comma(self):
        for vector, expected in [
            ([], ''),
            (['sugar'], 'sugar'),
            (['sugar', 'spice'], 'sugar and spice'),
            (['sugar', 'spice', 'everything nice'], 'sugar, spice, and everything nice'),
        ]:
            with self.subTest(vector=vector, expected=expected):
                result = hodgepodge.ux.join_with_oxford_comma(vector)
                self.assertEqual(result, expected)

    def test_join_with_oxford_comma_raises_typeerror_on_none(self):
        with self.assertRaises(TypeError):
            hodgepodge.ux.join_with_oxford_comma(None)

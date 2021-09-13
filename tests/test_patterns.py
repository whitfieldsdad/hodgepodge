from unittest import TestCase

import hodgepodge.patterns


class PatternMatchingTestCases(TestCase):

    def test_matches_regex_case_sensitive(self):
        result = hodgepodge.patterns.string_matches_regex("hello world", "[a-z ]+", case_sensitive=True)
        self.assertTrue(result)

    def test_matches_regex_case_insensitive(self):
        result = hodgepodge.patterns.string_matches_regex("hello world", "[a-z ]+", case_sensitive=False)
        self.assertTrue(result)

    def test_matches_glob_case_sensitive(self):
        result = hodgepodge.patterns.string_matches_glob("hello world", "hello*world", case_sensitive=True)
        self.assertTrue(result)

    def test_matches_glob_case_insensitive(self):
        result = hodgepodge.patterns.string_matches_glob("Hello World", "hello*world", case_sensitive=False)
        self.assertTrue(result)

    def test_any_string_matches_any_glob(self):
        for values, patterns, expected in (
            (['Dragonfly'], ['Dragonfly', 'Dragonfly', 'TG-4192', 'Crouching Yeti', 'IRON LIBERTY'], True),
            (['Dragonfly'], ['ALLANITE', 'ALLANITE', 'Palmetto Fusion'], False),
        ):
            with self.subTest(values=values, patterns=patterns):
                result = hodgepodge.patterns.any_string_matches_any_glob(values=values, patterns=patterns)
                self.assertEqual(expected, result)

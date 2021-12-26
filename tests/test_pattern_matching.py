from unittest import TestCase

import hodgepodge.pattern_matching


class PatternMatchingTestCases(TestCase):
    def test_matches_with_one_pattern(self):
        for values, patterns, case_sensitive, expected in (
            ('hello world', 'hello world', False, True),
            ('hello world', 'hello*', False, True),
            ('hello world', '*', False, True),
            ('Hello WorLD', '*hello*', False, True),
            ('Hello WorLD', '*hello*', True, False),
            ('', '', False, True),
            ('', '*', False, True),
            (None, '*', False, False),
        ):
            with self.subTest(values=values, patterns=patterns, case_sensitive=case_sensitive, expected=expected):
                result = hodgepodge.pattern_matching.matches(
                    values=values,
                    patterns=patterns,
                    case_sensitive=case_sensitive,
                )
                self.assertEqual(expected, result)

    def test_matches_with_multiple_patterns(self):
        for values, patterns, case_sensitive, expected in (
            ('hello world', ['hello world'], False, True),
            ('hello world', ['hello*'], False, True),
            ('hello world', ['*'], False, True),
            ('Hello WorLD', ['*hello*', 'doughnuts'], False, True),
            ('Hello WorLD', ['*hello*', 'world'], True, False),
            ('', '', False, True),
            ('', '*', False, True),
            (None, '*', False, False),
        ):
            with self.subTest(values=values, patterns=patterns, case_sensitive=case_sensitive, expected=expected):
                result = hodgepodge.pattern_matching.matches(
                    values=values,
                    patterns=patterns,
                    case_sensitive=case_sensitive,
                )
                self.assertEqual(expected, result)

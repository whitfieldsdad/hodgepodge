from typing import List

import fnmatch
import re


def string_matches_glob(value: str, pattern: str, case_sensitive: bool = True) -> bool:
    if not case_sensitive:
        value, pattern = map(str.lower, (value, pattern))
    return fnmatch.fnmatch(value, pattern)


def string_matches_any_glob(value: str, patterns: List[str], case_sensitive: bool = True) -> bool:
    for pattern in patterns:
        matches = string_matches_glob(
            value=value,
            pattern=pattern,
            case_sensitive=case_sensitive,
        )
        if matches:
            return True
    return False


def any_string_matches_any_glob(values: List[str], patterns: List[str], case_sensitive: bool = True) -> bool:
    if not case_sensitive:
        values = map(str.lower, values)
        patterns = map(str.lower, values)

    for value in values:
        for pattern in patterns:
            if string_matches_glob(value=value, pattern=pattern, case_sensitive=True):
                return True
    return False


def string_matches_regex(value: str, pattern: str, case_sensitive: bool = True) -> bool:
    flags = 0
    if not case_sensitive:
        flags |= re.IGNORECASE
    try:
        regex = re.compile(pattern, flags=flags)
    except re.error:
        return False
    else:
        return bool(regex.search(value))


def string_matches_any_regex(value: str, patterns: List[str], case_sensitive: bool = True) -> bool:
    for pattern in patterns:
        if string_matches_regex(value=value, pattern=pattern, case_sensitive=case_sensitive):
            return True
    return False


def any_string_matches_any_regex(values: List[str], patterns: List[str], case_sensitive: bool = True) -> bool:
    for value in values:
        for pattern in patterns:
            matches = string_matches_regex(value=value, pattern=pattern, case_sensitive=case_sensitive)
            if matches:
                return True
    return False

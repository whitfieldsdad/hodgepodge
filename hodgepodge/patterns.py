from typing import Iterable
from hodgepodge.constants import STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT

import fnmatch
import re


def string_matches_glob(value: str, pattern: str,
                        case_sensitive: bool = STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT) -> bool:
    if not case_sensitive:
        value = value.lower()
        pattern = pattern.lower()
    return fnmatch.fnmatch(value, pattern)


def string_matches_any_glob(value: str, patterns: Iterable[str],
                            case_sensitive: bool = STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT) -> bool:

    value = value.lower() if case_sensitive else value
    patterns = {pattern.lower() for pattern in patterns} if case_sensitive else set(patterns)

    for pattern in patterns:
        if string_matches_glob(value=value, pattern=pattern):
            return True
    return False


def any_string_matches_any_glob(values: Iterable[str], patterns: Iterable[str],
                                case_sensitive: bool = STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT) -> bool:

    values = {value.lower() for value in values} if case_sensitive else set(values)
    patterns = {pattern.lower() for pattern in patterns} if case_sensitive else set(patterns)

    for value in values:
        for pattern in patterns:
            if string_matches_glob(value=value, pattern=pattern, case_sensitive=case_sensitive):
                return True
    return False


def string_matches_regex(value: str, pattern: str,
                         case_sensitive: bool = STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT) -> bool:
    flags = 0
    if not case_sensitive:
        flags |= re.IGNORECASE
    try:
        regex = re.compile(pattern, flags=flags)
    except re.error:
        return False
    else:
        return bool(regex.search(value))


def string_matches_any_regex(value: str, patterns: Iterable[str],
                             case_sensitive: bool = STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT) -> bool:

    value = value.lower() if case_sensitive else value
    patterns = {pattern.lower() for pattern in patterns} if case_sensitive else set(patterns)

    for pattern in patterns:
        if string_matches_regex(value=value, pattern=pattern):
            return True
    return False


def any_string_matches_any_regex(values: Iterable[str], patterns: Iterable[str],
                                 case_sensitive: bool = STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT) -> bool:

    values = {value.lower() for value in values} if case_sensitive else set(values)
    patterns = {pattern.lower() for pattern in patterns} if case_sensitive else set(patterns)

    for value in values:
        for pattern in patterns:
            matches = string_matches_regex(
                value=value,
                pattern=pattern,
                case_sensitive=case_sensitive,
            )
            if matches:
                return True
    return False

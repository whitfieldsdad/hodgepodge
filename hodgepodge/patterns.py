from typing import Iterable, Union
from hodgepodge.constants import STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT

import fnmatch


def str_matches_glob(
        values: Union[str, Iterable[str]],
        patterns: Union[str, Iterable[str]],
        case_sensitive: bool = STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT) -> bool:

    if values is None or patterns is None:
        return False

    values = [values] if isinstance(values, str) else values
    patterns = [patterns] if isinstance(patterns, str) else patterns

    if not case_sensitive:
        values = list(map(str.lower, values))
        patterns = list(map(str.lower, patterns))

    for value in values:
        for pattern in patterns:
            if fnmatch.fnmatch(value, pattern):
                return True
    return False

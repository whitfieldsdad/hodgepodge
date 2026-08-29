from typing import Iterable


def multi_replace(s: str, old: Iterable[str], new: str):
    for v in old:
        s = s.replace(v, new)
    return s

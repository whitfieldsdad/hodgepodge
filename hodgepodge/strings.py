from typing import Iterable


def multi_replace(s: str, old: Iterable[str], new: str):
    for v in old:
        s = s.replace(v, new)
    return s


def replace_suffix(value: str, old: str, new: str) -> str:
    if value.endswith(old):
        value = value[: -len(old)] + new
    return value

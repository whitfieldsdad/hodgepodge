from typing import Any, Iterable, Iterator, Optional, Tuple


def iter_pairwise(iterable: Iterable[Any]) -> Iterator[Tuple[Any, Optional[Any]]]:
    """
    Iterate over `iterable` in pairs of consecutive elements.
    """
    iterable = iter(iterable)

    try:
        a = next(iterable)
    except StopIteration:
        return

    try:
        b = next(iterable)
    except StopIteration:
        yield (a, None)
        return

    yield (a, b)

    prev = b
    for item in iterable:
        yield (prev, item)
        prev = item


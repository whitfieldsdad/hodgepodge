from typing import Union, Optional


def is_within_range(
        value: Union[int, float],
        minimum: Optional[Union[int, float]] = None,
        maximum: Optional[Union[int, float]] = None) -> bool:

    if minimum is not None and value < minimum:
        return False
    if maximum is not None and value > maximum:
        return False
    return True

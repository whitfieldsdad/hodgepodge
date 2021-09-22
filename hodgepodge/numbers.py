from typing import Union, Optional


def is_within_range(value: Union[int, float], minimum: Optional[int, float] = None, maximum: Optional[int, float] = None):
    if minimum is not None and value < minimum:
        return False
    if maximum is not None and value > maximum:
        return False
    return True

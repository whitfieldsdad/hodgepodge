from typing import List


def str_to_strs(data: str) -> List[str]:
    if not data:
        return []
    return data.split(',')


def str_to_ints(data: str) -> List[int]:
    return [int(v) for v in str_to_strs(data)]

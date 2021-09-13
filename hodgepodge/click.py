from typing import List


def str_to_list(data: str) -> List[str]:
    return str_to_list_of_str(data)


def str_to_list_of_str(data: str) -> List[str]:
    if not data:
        return []
    return data.split(',')


def str_to_list_of_int(data: str) -> List[int]:
    return [int(v) for v in str_to_list_of_str(data)]

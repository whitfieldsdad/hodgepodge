from typing import List, Optional


def str_to_list(data: Optional[str]) -> List[str]:
    if data is None:
        return []
    return data.split(',')

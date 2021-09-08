from typing import Union, List, Optional

import click
import hodgepodge.types
import hodgepodge.json


def echo(data: Union[str, List[dict], dict]) -> None:
    if isinstance(data, (str, bytes, bytearray)):
        if not data:
            return
    elif isinstance(data, (int, float)):
        pass
    elif isinstance(data, dict):
        data = hodgepodge.types.dict_to_json(data)
    elif hodgepodge.types.is_iterator(data):
        for row in data:
            echo(row)
        return
    else:
        raise TypeError("Unsupported type: {} ({})", type(data).__name__, data)
    click.echo(data)


def str_to_list(data: Optional[str]) -> List[str]:
    if data is None:
        return []
    return data.split(',')

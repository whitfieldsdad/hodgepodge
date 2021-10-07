from typing import List, Iterable, Union

import hodgepodge.time
import hodgepodge.types
import click
import json


def str_to_strs(data: str) -> List[str]:
    if not data:
        return []
    return data.split(',')


def str_to_ints(data: str) -> List[int]:
    return [int(v) for v in str_to_strs(data)]


def echo_as_json(data: Union[dict, Iterable[dict]]) -> None:
    if isinstance(data, dict):
        txt = json.dumps(data)
        click.echo(txt)
    elif hodgepodge.types.is_iterator(data):
        for row in data:
            echo_as_json(row)
    else:
        raise TypeError(type(data))

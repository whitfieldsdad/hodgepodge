import json
from typing import List, Any

import click

import hodgepodge.types


def str_to_list(data: str) -> List[str]:
    return str_to_list_of_str(data)


def str_to_list_of_str(data: str) -> List[str]:
    if not data:
        return []
    return data.split(',')


def str_to_list_of_int(data: str) -> List[int]:
    return [int(v) for v in str_to_list_of_str(data)]


def echo_len(rows: Any) -> None:
    total = hodgepodge.types.get_len(rows)
    click.echo(total)


def echo_as_json(rows: Any) -> None:
    if hodgepodge.types.is_iterator(rows):
        rows = list(rows)
    txt = json.dumps(rows)
    click.echo(txt)


def echo_as_jsonl(rows: Any) -> None:
    for row in rows:
        txt = json.dumps(row)
        click.echo(txt)

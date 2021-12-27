from typing import Any, Union, Dict, Iterable, Iterator, Set, Optional, Tuple
from hodgepodge.serialization import JSONEncoder

import itertools
import collections
import dataclasses
import distutils.util
import json


def iterate_in_chunks(iterable: Iterable[Any], chunk_size: int) -> Iterator[Tuple]:
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, chunk_size))
        if not chunk:
            return
        yield chunk


def get_dotted_dict_keys(data: dict, parent: Optional[str] = None) -> Set[str]:
    keys = set()
    for key, value in data.items():
        if parent:
            key = '{}.{}'.format(parent, key)
        keys.add(key)

        if isinstance(value, dict):
            keys |= get_dotted_dict_keys(value, parent=key)
    return keys


def filter_dict(data: dict, keys: Iterable[str]) -> dict:
    if keys:
        keys = set(keys)
        data = dict((k, v) for (k, v) in data.items() if k in keys)
    return data


def filter_dict_stream(stream: Iterable[dict], keys: Iterable[str]) -> Iterator[dict]:
    for row in stream:
        row = filter_dict(data=row, keys=keys)
        if row:
            yield row


def get_length(data: Any) -> int:
    if is_iterator(data):
        return sum(1 for _ in data)
    return len(data)


def is_iterable(data: Any) -> bool:
    try:
        iter(data)
    except TypeError:
        return False
    else:
        return True


def is_iterator(data: Any) -> bool:
    a = data
    try:
        b = iter(data)
    except TypeError:
        return False
    else:
        return a is b


def str_to_bool(string: str) -> bool:
    if isinstance(string, bool):
        return string
    return bool(distutils.util.strtobool(string))


def str_to_bytes(string: str, encoding: str = 'utf-8', errors: str = 'surrogateescape') -> bytes:
    return string.encode(encoding=encoding, errors=errors)


def int_to_bytes(x: int, byteorder: str = 'big') -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, byteorder=byteorder)


def int_from_bytes(x: bytes, byteorder='big') -> int:
    return int.from_bytes(x, byteorder=byteorder)


def bytes_to_hex(value: bytes) -> str:
    return value.hex()


def bytes_to_str(data: Any, encoding: str = 'utf-8', errors: str = 'surrogateescape') -> str:
    return data.decode(encoding=encoding, errors=errors)


def dataclass_to_json(data: Any, remove_empty_values: bool = False, sort_keys: bool = False,
                      indent: Union[int, None] = None) -> str:
    data = dataclass_to_dict(data, remove_empty_values=remove_empty_values)
    return dict_to_json(data, indent=indent, sort_keys=sort_keys)


def dataclass_to_dict(data: Any, remove_empty_values: bool = False, preserve_order: bool = False) -> Dict[Any, Any]:
    if preserve_order:
        factory = collections.OrderedDict
    else:
        factory = dict

    new = factory((field.name, getattr(data, field.name)) for field in dataclasses.fields(data))
    if remove_empty_values:
        new = remove_empty_values_from_dict(new)
    return new


def dict_to_dataclass(data: Any, data_class: Any) -> Any:
    non_init_fields = frozenset((f.name for f in dataclasses.fields(data_class) if f.init is False))
    if non_init_fields:
        for k in non_init_fields:
            if k in data:
                del data[k]
    return data_class(**data)


def dict_to_json(data: dict, indent: Union[int, None] = None, sort_keys: bool = True,
                 remove_empty_values: bool = False) -> str:

    if remove_empty_values:
        data = remove_empty_values_from_dict(data)
    return json.dumps(data, indent=indent, sort_keys=sort_keys, cls=JSONEncoder)


def to_json(data: Any, indent: Union[int, None] = None, sort_keys: bool = True) -> str:
    if isinstance(data, dataclasses.is_dataclass(data)):
        data = dataclass_to_dict(data)
    return dict_to_json(data=data, indent=indent, sort_keys=sort_keys)


def json_to_dict(data: str) -> Dict[Any, Any]:
    return json.loads(data)


def json_to_dataclass(data: str, data_class: Any) -> Any:
    data = json_to_dict(data)
    return dict_to_dataclass(data=data, data_class=data_class)


def remove_empty_values_from_dict(data: dict) -> Dict[Any, Any]:
    output = {}
    for key, value in data.items():
        if value:
            if is_iterable(value) and isinstance(value, (str, bytes, bytearray)) is False:
                if all(isinstance(entry, dict) for entry in value):
                    entries = []
                    for entry in value:
                        entry = remove_empty_values_from_dict(entry)
                        entries.append(entry)
                    value = entries
            output[key] = value
        elif isinstance(value, (bool, int, float)):
            output[key] = value
        else:
            continue
    return output

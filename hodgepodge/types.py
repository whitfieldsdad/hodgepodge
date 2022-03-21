from typing import Any, Union, Dict, Iterable, Iterator, Set, Optional, Tuple
from hodgepodge.constants import DEFAULT_JSON_INDENT, SORT_JSON_KEYS_BY_DEFAULT
from hodgepodge.serialization import JSONEncoder

import itertools
import collections
import dataclasses
import distutils.util
import json

DEFAULT_CHUNK_SIZE = 500


def get_nested_keys(data: dict, sep='.') -> Set[str]:
    return set(_iter_nested_keys(data=data, sep=sep))


def _iter_nested_keys(data: dict, parent_key: Optional[str] = None, sep='.') -> Set[str]:
    for key, value in data.items():
        if parent_key:
            key = '{}{}{}'.format(parent_key, sep, key)
        yield key

        if isinstance(value, dict):
            yield from _iter_nested_keys(value, parent_key=key)


def chunk_iter(it: Iterable[Any], n: Optional[int] = DEFAULT_CHUNK_SIZE) -> Iterator[Tuple]:
    it = iter(it)
    while True:
        c = tuple(itertools.islice(it, n))
        if not c:
            return
        yield c


def get_size(data: Any) -> int:
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


def dataclass_to_json(data: Any, sort_keys: bool = False, indent: Union[int, None] = None) -> str:
    data = dataclass_to_dict(data)
    return dict_to_json(data, indent=indent, sort_keys=sort_keys)


def dataclass_to_dict(data: Any, preserve_order: bool = False) -> Dict[Any, Any]:
    if preserve_order:
        factory = collections.OrderedDict
    else:
        factory = dict

    new = factory((field.name, getattr(data, field.name)) for field in dataclasses.fields(data))
    return new


def dict_to_dataclass(data: Any, cls: Any) -> Any:
    fields = dataclasses.fields(cls)
    non_init_fields = frozenset((f.name for f in fields if f.init is False))
    if non_init_fields:
        for k in non_init_fields:
            if k in data:
                del data[k]

    fields = {f.name for f in fields}
    data = dict(((k, v) for (k, v) in data.items() if k in fields))
    return cls(**data)


def dict_to_json(data: dict, indent: Optional[int] = 4, sort_keys: bool = True) -> str:
    return json.dumps(data, indent=indent, sort_keys=sort_keys, cls=JSONEncoder)


def to_json(data: Any, indent: Optional[int] = DEFAULT_JSON_INDENT, sort_keys: bool = SORT_JSON_KEYS_BY_DEFAULT) -> str:
    return dict_to_json(data=data, indent=indent, sort_keys=sort_keys)


def json_to_dict(data: str) -> Dict[str, Any]:
    return json.loads(data)


def json_to_dataclass(data: str, data_class: Any) -> Any:
    data = json_to_dict(data)
    return dict_to_dataclass(data=data, cls=data_class)


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

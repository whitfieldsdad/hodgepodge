from typing import Any, Union, Dict

import hodgepodge.json
import collections
import dacite
import dataclasses
import distutils.util
import json


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
        dict_factory = collections.OrderedDict
    else:
        dict_factory = dict

    new = dataclasses.asdict(data, dict_factory=dict_factory)
    if remove_empty_values:
        new = remove_empty_values_from_dict(new)
    return new


def dict_to_dataclass(data: Any, data_class: Any, ignore_extra_keys: bool = True) -> Any:
    non_init_fields = frozenset((f.name for f in dataclasses.fields(data_class) if f.init is False))
    if non_init_fields:
        for k, v in data.items():
            if k in non_init_fields:
                del data[k]

    if ignore_extra_keys:
        config = dacite.Config(strict=False)
    else:
        config = dacite.Config(strict=True)

    try:
        data = dacite.from_dict(data=data, data_class=data_class, config=config)
    except dacite.exceptions.UnexpectedDataError as exception:
        raise ValueError(exception)
    else:
        return data


def dict_to_json(data: dict, indent: Union[int, None] = None, sort_keys: bool = True,
                 remove_empty_values: bool = False) -> str:

    if remove_empty_values:
        data = remove_empty_values_from_dict(data)
    return json.dumps(data, indent=indent, sort_keys=sort_keys, default=hodgepodge.json.custom_json_serializer)


def to_json(data: Any, indent: Union[int, None] = None, sort_keys: bool = True) -> str:
    if isinstance(data, dataclasses.is_dataclass(data)):
        data = dataclass_to_dict(data)
    return dict_to_json(data=data, indent=indent, sort_keys=sort_keys)


def json_to_dict(data: str) -> Dict[Any, Any]:
    return json.loads(data)


def json_to_dataclass(data: str, data_class: Any, ignore_extra_keys: bool = True) -> Any:
    data = json_to_dict(data)
    return dict_to_dataclass(data=data, data_class=data_class, ignore_extra_keys=ignore_extra_keys)


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

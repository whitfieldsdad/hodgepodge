from json import JSONEncoder as _JSONEncoder

import dataclasses
import datetime

import hodgepodge.types


class Serializable:
    def to_dict(self, remove_empty_values: bool = False):
        data = self.__dict__
        if remove_empty_values:
            data = hodgepodge.types.remove_empty_values_from_dict(data)
        return data

    def to_json(self, remove_empty_values: bool = False):
        data = self.to_dict(remove_empty_values=remove_empty_values)
        return hodgepodge.types.dict_to_json(data)


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        elif dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif callable(o):
            return
        return super().default(o)

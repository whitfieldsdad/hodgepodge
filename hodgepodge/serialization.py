from json import JSONEncoder as _JSONEncoder

import dataclasses
import datetime


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        elif dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif callable(o):
            return
        return super().default(o)

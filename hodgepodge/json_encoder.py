import dataclasses
import datetime
import json


class JSONEncoder(json.JSONEncoder):
    """
    A custom JSON encoder that supports:
    
    - `datetime.date` and `datetime.datetime` objects, which are serialized to ISO format strings.
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        else:
            return super().default(obj)

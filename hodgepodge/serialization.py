from typing import Any

import datetime


def custom_json_serializer(obj: Any):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    elif callable(obj):
        return
    raise TypeError("Type {} not serializable".format(type(obj)))

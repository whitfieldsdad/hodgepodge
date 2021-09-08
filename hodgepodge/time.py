from typing import Any, Union, Optional

import collections
import datetime
import dateutil.parser
import time

Time = collections.namedtuple('Time', ['years', 'days', 'hours', 'minutes', 'seconds'])


def now():
    return time.time()


def is_within_range(timestamp: float, minimum: float = None, maximum: float = None):
    if minimum is not None and timestamp < minimum:
        return False
    if maximum is not None and timestamp > maximum:
        return False
    return True


def parse_timestamp(timestamp: Any) -> Optional[float]:
    return as_epoch_timestamp(timestamp)


def as_epoch_timestamp(timestamp: Any) -> Optional[float]:
    t = timestamp
    if timestamp is None:
        return None
    elif isinstance(t, float):
        return t
    elif isinstance(t, int):
        return float(t)
    elif hasattr(t, "timestamp"):
        if callable(getattr(t, "timestamp")):
            return as_epoch_timestamp(t.timestamp())
        else:
            return as_epoch_timestamp(t.timestamp)
    else:
        return dateutil.parser.parse(timestamp).timestamp()


def as_duration(seconds: Union[int, float, datetime.timedelta]) -> Time:
    if isinstance(seconds, datetime.timedelta):
        return as_duration(seconds.total_seconds())
    elif isinstance(seconds, (int, float)) is False:
        raise TypeError("Unsupported types: {}".format(type(seconds).__name__))

    days, seconds = divmod(seconds, 24 * 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    years, days = divmod(days, 365)

    return Time(
        years=int(years),
        days=int(days),
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
    )

from typing import Union, Optional
from hodgepodge.objects.host.time_parts import TimeParts

import datetime
import arrow
import dateutil.parser
import time as _time


def get_current_time_as_epoch_time_in_fractional_seconds() -> float:
    """
    Gets the current time as an epoch timestamp.

    :return: a floating point representation as the number of seconds since the epoch with nanosecond precision.
    """
    return _time.time()


def get_current_time_as_date() -> datetime.date:
    """
    Get the current date.

    :return: a datetime.date object representing the current date.
    """
    return datetime.date.today()


def get_current_time_as_datetime() -> datetime.datetime:
    """
    Get the current time as a datetime object.

    :return: a datetime.datetime object representing the current time.
    """
    return datetime.datetime.now()


def convert_time_to_epoch_time_in_fractional_seconds(
        timestamp: Union[int, float, datetime.datetime, datetime.date, arrow.Arrow, None]) -> Optional[float]:
    """
    Convert the provided timestamp into the fractional number of seconds since the epoch.

    :param timestamp: a timestamp.
    :return: a floating point representation of the number of seconds since the epoch (i.e. January 1st, 1970).
    """
    t = timestamp
    if t is None:
        return None

    if isinstance(t, str):
        t = dateutil.parser.parse(t).timestamp()
    elif isinstance(t, float):
        pass
    elif isinstance(t, int):
        t = float(t)
    elif isinstance(t, (arrow.Arrow, datetime.date, datetime.datetime)):
        t = t.timestamp()
    elif hasattr(t, 'timestamp'):
        if callable(t.timestamp):
            t = timestamp.timestamp()
        else:
            t = timestamp.timestamp
    else:
        raise TypeError("Unsupported timestamp format: %s (%s)", str(t), type(t).__name__)
    return t


def convert_time_to_datetime(
        timestamp: Union[str, int, float, datetime.datetime, datetime.date, arrow.Arrow, None]) -> Optional[datetime.datetime]:
    """
    Convert the provided timestamp into a datetime.

    :param timestamp: a timestamp
    :return: a datetime.
    """
    if timestamp is None:
        return None
    elif isinstance(timestamp, str):
        return dateutil.parser.parse(timestamp)
    else:
        seconds = convert_time_to_epoch_time_in_fractional_seconds(timestamp)
        return datetime.datetime.fromtimestamp(seconds)


def convert_time_to_date(
        timestamp: Union[int, float, datetime.datetime, datetime.date, arrow.Arrow, None]) -> Optional[datetime.date]:
    """
    Convert the provided timestamp into a date.

    :param timestamp: a timestamp
    :return: a date.
    """
    if timestamp is None:
        return None

    seconds = convert_time_to_epoch_time_in_fractional_seconds(timestamp)
    return datetime.date.fromtimestamp(seconds)


def is_within_range(
        time: Union[str, int, float, datetime.datetime, datetime.date, arrow.Arrow],
        minimum: Union[str, int, float, datetime.datetime, datetime.date, arrow.Arrow, None] = None,
        maximum: Union[str, int, float, datetime.datetime, datetime.date, arrow.Arrow, None] = None) -> bool:
    """
    Determines whether or not the provided timestamps falls within the provided timeframe.

    :param time: a timestamp.
    :param minimum: an optional minimum time
    :param maximum: an optional maximum time.
    :return: True if the provided timestamp falls within the provided timeframe and False otherwise.
    """
    time, minimum, maximum = map(convert_time_to_datetime, (time, minimum, maximum))
    if minimum and time < minimum:
        return False
    if maximum and time > maximum:
        return False
    return True


def convert_time_to_parts(seconds: Union[int, float, datetime.timedelta]) -> TimeParts:
    """
    Slice and dice the provided timestamp into the number of years, days, hours, minutes, seconds, and milliseconds
    since the epoch.

    :param seconds: the number of seconds since the epoch (i.e. January 1st, 1970).
    :return: a named tuple of the form (years, days, hours, minutes, seconds, milliseconds).
    """
    if isinstance(seconds, datetime.timedelta):
        return convert_time_to_parts(seconds.total_seconds())
    elif not isinstance(seconds, (int, float)):
        raise TypeError("Unsupported types: {}".format(type(seconds).__name__))

    days, seconds = divmod(seconds, 24 * 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    years, days = divmod(days, 365)

    return TimeParts(
        years=int(years),
        days=int(days),
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
    )

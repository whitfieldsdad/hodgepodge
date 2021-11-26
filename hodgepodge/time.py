from typing import Union, Optional
from dataclasses import dataclass

import datetime
import arrow
import dateutil.parser
import time

HOUR = 'hour'
DAY = 'day'
MONTH = 'month'


@dataclass()
class Duration:
    years: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0

    def to_datetime(self) -> datetime.datetime:
        seconds = sum((
            self.seconds,
            self.minutes * 60,
            self.hours * 60 * 60,
            self.days * 24 * 60 * 60,
            self.years * 24 * 60 * 60 * 365,
        ))
        return datetime.datetime.fromtimestamp(seconds)

    def __iter__(self):
        return iter((self.years, self.days, self.hours, self.minutes, self.seconds))


def current_time_as_date() -> datetime.date:
    return datetime.date.today()


def current_time_as_datetime() -> datetime.datetime:
    return datetime.datetime.now()


def current_time_as_arrow() -> arrow.Arrow:
    return arrow.now()


def current_time_as_epoch_time() -> float:
    return time.time()


def to_epoch_time(timestamp: Union[str, int, float, datetime.date, arrow.Arrow, None] = None) -> Optional[float]:
    if timestamp is not None:
        return to_datetime(timestamp).timestamp()


def to_date(timestamp: Union[str, int, float, datetime.date, arrow.Arrow, None] = None) -> Optional[datetime.date]:
    t = to_datetime(timestamp)
    return t.date()


def to_datetime(timestamp: Union[str, int, float, datetime.date, arrow.Arrow, None]) -> Optional[datetime.datetime]:
    t = timestamp
    if t is None:
        return t
    elif isinstance(t, str):
        return dateutil.parser.parse(t)
    elif isinstance(t, (int, float)):
        return datetime.datetime.fromtimestamp(t)
    elif isinstance(t, datetime.datetime):
        return t
    elif isinstance(t, datetime.date):
        return datetime.datetime.combine(t, datetime.datetime.min.time())
    elif isinstance(t, arrow.Arrow):
        return t.datetime
    else:
        raise TypeError("Unsupported timestamp format: %s", type(t).__name__)


def to_duration(seconds: Union[int, float, datetime.timedelta]) -> Duration:
    if isinstance(seconds, datetime.timedelta):
        return to_duration(seconds.total_seconds())
    elif not isinstance(seconds, (int, float)):
        raise TypeError("Unsupported types: {}".format(type(seconds).__name__))

    days, seconds = divmod(seconds, 24 * 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    years, days = divmod(days, 365)

    return Duration(
        years=int(years),
        days=int(days),
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
    )


def in_range(
        timestamp: Union[str, int, float, datetime.datetime, datetime.date, arrow.Arrow],
        minimum: Union[str, int, float, datetime.datetime, datetime.date, arrow.Arrow, None] = None,
        maximum: Union[str, int, float, datetime.datetime, datetime.date, arrow.Arrow, None] = None) -> bool:

    timestamp, minimum, maximum = map(to_epoch_time, (timestamp, minimum, maximum))
    if minimum and timestamp < minimum:
        return False
    if maximum and timestamp > maximum:
        return False
    return True


def round_datetime(timestamp: datetime.datetime, granularity: str) -> datetime.datetime:
    if granularity == HOUR:
        timestamp = timestamp.replace(microsecond=0, second=0, minute=0)
    elif granularity == DAY:
        timestamp = timestamp.replace(microsecond=0, second=0, minute=0, hour=0)
    elif granularity == MONTH:
        timestamp = timestamp.replace(microsecond=0, second=0, minute=0, hour=0, day=1)
    else:
        raise ValueError("Unsupported granularity: '{}' (supported: {})".format(granularity, [HOUR, DAY, MONTH]))
    return timestamp

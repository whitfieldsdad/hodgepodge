import datetime
from typing import Iterator, Optional, Union


def iter_dates(
        min_date: Union[str, datetime.date], 
        max_date: Optional[Union[str, datetime.date]] = None) -> Iterator[datetime.date]:
    """
    Iterate over all dates in the specified range.
    
    If no max_date is provided, defaults to today's date.
    """
    min_date = parse_date(min_date)
    max_date = parse_date(max_date) if max_date else datetime.date.today()
    delta = max_date - min_date
    for i in range(delta.days + 1):
        day = min_date + datetime.timedelta(days=i)
        yield day


def parse_date(d: Optional[Union[str, datetime.date]]) -> Optional[datetime.date]:
    """
    Parse the provided date.
    """
    if d is not None:
        dt = parse_datetime(d)
        if dt is not None:
            return dt.date()


def parse_datetime(dt: Optional[Union[str, datetime.date, int, float]]) -> Optional[datetime.datetime]:
    """
    Parse the provided datetime.
    """
    if dt is not None:
        if isinstance(dt, datetime.datetime):
            return dt
        elif isinstance(dt, datetime.date):
            return datetime.datetime.combine(dt, datetime.time())
        elif isinstance(dt, str):
            try:
                return datetime.datetime.fromisoformat(dt)
            except ValueError:
                raise ValueError(f"Unsupported timestamp format: {dt}")
        elif isinstance(dt, (int, float)):
            return datetime.datetime.fromtimestamp(dt)
        else:
            raise ValueError(f"Unsupported timestamp format: {dt}")

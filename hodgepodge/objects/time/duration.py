from dataclasses import dataclass

import datetime


@dataclass(frozen=True)
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
        return iter([self.years, self.days, self.hours, self.minutes, self.seconds])

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeParts:
    years: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0

    def __iter__(self):
        return iter([self.years, self.days, self.hours, self.minutes, self.seconds])

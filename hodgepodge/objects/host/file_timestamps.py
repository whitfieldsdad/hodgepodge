from dataclasses import dataclass

import datetime


@dataclass(frozen=True)
class FileTimestamps:
    last_modified_time: datetime.datetime
    last_accessed_time: datetime.datetime
    last_changed_time: datetime.datetime

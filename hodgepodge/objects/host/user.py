from dataclasses import dataclass, field
from typing import List, Optional

import datetime


@dataclass(frozen=True)
class User:
    time: datetime.datetime
    id: str
    name: Optional[str] = field(default=None)
    group_ids: List[str] = field(default_factory=list)

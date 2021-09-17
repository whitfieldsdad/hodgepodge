from dataclasses import dataclass, field
from typing import List, Optional

import datetime


@dataclass(frozen=True)
class Group:
    time: datetime.datetime
    id: str
    name: Optional[str] = field(default=None)
    user_ids: List[str] = field(default_factory=list)

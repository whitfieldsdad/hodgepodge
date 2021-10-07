from dataclasses import dataclass, field
from typing import List, Optional, Iterable, Iterator

import datetime
import pwd
import grp


@dataclass(frozen=True)
class User:
    id: str
    time: datetime.datetime
    name: Optional[str] = field(default=None)
    group_ids: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Group:
    id: str
    time: datetime.datetime
    name: Optional[str] = field(default=None)
    user_ids: List[str] = field(default_factory=list)


def get_users() -> Iterable[User]:
    return list(iter_users())


def iter_users() -> Iterator[User]:
    for row in pwd.getpwall():
        name, _, uid, gid, _, _, _ = row
        yield User(
            id=uid,
            time=datetime.datetime.now(),
            name=name,
            group_ids=[gid]
        )


def def_groups() -> Iterable[Group]:
    return list(iter_groups())


def iter_groups() -> Iterator[Group]:
    user_ids = dict((u.name, u.id) for u in iter_users())
    for row in grp.getgrall():
        name, _, gid, usernames = row
        user_ids = list(set(filter(bool, (user_ids.get(name) for name in usernames))))

        yield Group(
            id=gid,
            time=datetime.datetime.now(),
            name=name,
            user_ids=user_ids,
        )

from dataclasses import dataclass, field
from typing import List, Optional, Iterable, Iterator
from hodgepodge.serialization import Serializable

import pwd
import grp


@dataclass(frozen=True)
class User(Serializable):
    id: str
    username: Optional[str] = field(default=None)
    group_ids: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Group(Serializable):
    id: str
    name: Optional[str] = field(default=None)
    user_ids: List[str] = field(default_factory=list)


def iter_users(
        user_ids: Optional[Iterable[int]] = None,
        group_ids: Optional[Iterable[int]] = None,
        usernames: Optional[Iterable[str]] = None) -> Iterator[User]:

    for row in pwd.getpwall():
        username, _, uid, gid, _, _, _ = row

        #: Filter users by user ID.
        if user_ids and uid not in user_ids:
            continue

        #: Filters users by group ID.
        if group_ids and gid not in group_ids:
            continue

        #: Filter users by username.
        if usernames and username not in usernames:
            continue

        yield User(
            id=uid,
            username=username,
            group_ids=[gid]
        )


def get_user(user_id: Optional[int] = None, username: Optional[str] = None) -> Optional[User]:
    user_ids = [user_id] if user_id is not None else []
    usernames = [username] if username else None

    users = iter_users(
        user_ids=user_ids,
        usernames=usernames,
    )
    user = next(users, None)
    return user


def iter_groups(group_ids: Optional[Iterable[int]] = None) -> Iterator[Group]:
    usernames_to_user_ids = dict((u.username, u.id) for u in iter_users())
    for row in grp.getgrall():
        name, _, gid, usernames = row

        #: Filter groups by group ID.
        if group_ids and gid not in group_ids:
            continue

        user_ids = usernames_to_user_ids.get(name, [])

        yield Group(
            id=gid,
            name=name,
            user_ids=user_ids,
        )

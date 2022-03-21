from dataclasses import dataclass, field
from typing import List, Optional, Iterable, Iterator

import collections
import logging
import pwd
import grp

logger = logging.getLogger(__name__)


@dataclass()
class User:
    id: int
    username: Optional[str] = None
    group_ids: List[int] = field(default_factory=list)

    @property
    def name(self) -> Optional[str]:
        return self.username


@dataclass(frozen=True)
class Group:
    id: int
    name: Optional[str] = None
    user_ids: List[int] = field(default_factory=list)


def iter_users(
        user_ids: Optional[Iterable[int]] = None,
        group_ids: Optional[Iterable[int]] = None,
        usernames: Optional[Iterable[str]] = None) -> Iterator[User]:

    user_ids = set(user_ids) if user_ids else None
    group_ids = set(group_ids) if group_ids else None
    usernames = set(usernames) if usernames else None

    user_names_to_group_ids = collections.defaultdict(set)
    for group in grp.getgrall():
        gid = group.gr_gid
        for username in group.gr_mem:
            user_names_to_group_ids[username].add(gid)

    for row in pwd.getpwall():
        username, _, uid, gid, _, _, _ = row
        gids = user_names_to_group_ids.get(username, {gid})

        #: Filter users by user ID.
        if user_ids and uid not in user_ids:
            continue

        #: Filters users by group ID.
        if group_ids and gids.isdisjoint(group_ids):
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


def get_group(group_id: Optional[int] = None, name: Optional[str] = None) -> Optional[Group]:
    group_ids = {group_id} if group_id else None
    names = {name} if name else None

    groups = iter_groups(group_ids=group_ids, names=names)
    return next(groups, None)


def iter_groups(
        group_ids: Optional[Iterable[int]] = None,
        names: Optional[Iterable[int]] = None,
        user_ids: Optional[Iterable[int]] = None) -> Iterator[Group]:

    usernames_to_user_ids = dict((u.username, u.id) for u in iter_users())
    for row in grp.getgrall():
        name, _, gid, usernames = row

        #: Filter groups by group ID.
        if group_ids and gid not in group_ids:
            continue

        #: Filter groups by group name.
        if names and name not in names:
            continue

        #: Filter groups by user ID.
        uids = set(filter(bool, map(usernames_to_user_ids.get, usernames)))
        if user_ids and uids.isdisjoint(user_ids):
            continue

        yield Group(
            id=gid,
            name=name,
            user_ids=sorted(uids),
        )

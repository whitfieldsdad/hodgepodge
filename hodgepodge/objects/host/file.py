from typing import Dict, Optional, List
from dataclasses import dataclass
from hodgepodge.objects.host.file_stat_result import FileStatResult
from hodgepodge.objects.host.file_timestamps import FileTimestamps
from hodgepodge.objects.host.group import Group
from hodgepodge.objects.host.user import User

import hodgepodge.files
import hodgepodge.time
import datetime


@dataclass()
class File:
    time: datetime.datetime
    path: str
    real_path: str
    stat_result: FileStatResult
    hashes: Optional[Dict[str, str]] = None

    @property
    def name(self):
        return hodgepodge.files.get_base_name(self.path)

    @property
    def names(self):
        paths = set()
        for path in [self.path, self.real_path]:
            if path:
                name = hodgepodge.files.get_base_name(path)
                paths.update({path, name})
        return list(paths)

    @property
    def mode(self) -> int:
        return self.stat_result.mode

    @property
    def inode_number(self) -> int:
        return self.stat_result.file_inode_number

    @property
    def device_inode_number(self) -> int:
        return self.stat_result.device_inode_number

    @property
    def number_of_links(self) -> int:
        return self.stat_result.number_of_links

    @property
    def owner(self) -> User:
        uid = str(self.stat_result.st_uid)
        gid = str(self.stat_result.st_gid)

        return User(
            time=self.time,
            id=uid,
            group_ids=[gid],
        )

    @property
    def related_users(self) -> List[User]:
        return [self.owner]

    @property
    def related_groups(self) -> List[Group]:
        gid = str(self.stat_result.st_gid)
        return [
            Group(time=self.time, id=gid),
        ]

    @property
    def size(self) -> int:
        return self.stat_result.size

    @property
    def timestamps(self) -> FileTimestamps:
        return self.stat_result.timestamps

    @property
    def last_modified_time(self) -> datetime.datetime:
        return self.stat_result.last_modified_time

    @property
    def last_accessed_time(self) -> datetime.datetime:
        return self.stat_result.last_accessed_time

    @property
    def last_changed_time(self) -> datetime.datetime:
        return self.stat_result.last_changed_time

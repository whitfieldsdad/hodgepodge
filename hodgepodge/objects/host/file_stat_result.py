from dataclasses import dataclass
from hodgepodge.objects.host.file_timestamps import FileTimestamps

import hodgepodge.time
import datetime


@dataclass(frozen=True)
class FileStatResult:
    st_mode: int
    st_ino: int
    st_dev: int
    st_nlink: int
    st_uid: int
    st_gid: int
    st_size: int
    st_atime: float
    st_mtime: float
    st_ctime: float

    @property
    def mode(self) -> int:
        return self.st_mode

    @property
    def file_inode_number(self) -> int:
        return self.st_ino

    @property
    def device_inode_number(self) -> int:
        return self.st_dev

    @property
    def number_of_links(self) -> int:
        return self.st_nlink

    @property
    def size(self) -> int:
        return self.st_size

    @property
    def timestamps(self) -> FileTimestamps:
        return FileTimestamps(
            last_modified_time=self.last_modified_time,
            last_accessed_time=self.last_accessed_time,
            last_changed_time=self.last_changed_time,
        )

    @property
    def last_modified_time(self) -> datetime.datetime:
        return hodgepodge.time.convert_time_to_datetime(self.st_mtime)

    @property
    def last_accessed_time(self) -> datetime.datetime:
        return hodgepodge.time.convert_time_to_datetime(self.st_atime)

    @property
    def last_changed_time(self) -> datetime.datetime:
        return hodgepodge.time.convert_time_to_datetime(self.st_ctime)

    def get_mode(self) -> int:
        return self.mode

    def get_file_inode_number(self) -> int:
        return self.file_inode_number

    def get_device_inode_number(self) -> int:
        return self.device_inode_number

    def get_number_of_links(self) -> int:
        return self.number_of_links

    def get_size(self) -> int:
        return self.size

    def get_timestamps(self) -> FileTimestamps:
        return self.timestamps

    def get_last_modified_time(self) -> datetime.datetime:
        return self.get_last_modified_time()

    def get_last_accessed_time(self) -> datetime.datetime:
        return self.get_last_accessed_time()

    def get_last_changed_time(self) -> datetime.datetime:
        return self.get_last_changed_time()

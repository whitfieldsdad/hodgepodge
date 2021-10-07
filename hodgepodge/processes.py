from typing import Optional, Iterable, Iterator
from dataclasses import dataclass

import psutil
import hodgepodge.pattern_matching
import hodgepodge.hashing
import datetime


@dataclass(frozen=True)
class Process:
    time: datetime.datetime
    pid: int
    ppid: int
    name: Optional[str]

    def id(self):
        return hodgepodge.hashing.get_md5('{}:{}'.format(self.pid, self.ppid))


def get_processes(
        pids: Optional[Iterable[int]],
        ppids: Optional[Iterable[int]] = None,
        names: Optional[Iterable[str]] = None) -> Iterable[Process]:

    return list(iter_processes(
        pids=pids,
        ppids=ppids,
        names=names,
    ))


def iter_processes(
        pids: Optional[Iterable[int]],
        ppids: Optional[Iterable[int]] = None,
        names: Optional[Iterable[str]] = None) -> Iterator[Process]:

    pids, ppids, names = map(set, (pids, ppids, names))

    #: Iterate through all processes.
    for process in psutil.process_iter():
        pid = process.pid
        ppid = process.ppid()
        name = process.name()

        #: Filter by PID.
        if pids and process.pid not in pids:
            continue

        #: Filter by PPID.
        if ppids and ppid not in ppids:
            continue

        #: Filter by name.
        if names and not hodgepodge.pattern_matching.str_matches_glob(name, names):
            continue

        yield Process(
            time=datetime.datetime.now(),
            pid=pid,
            ppid=ppid,
            name=name,
        )

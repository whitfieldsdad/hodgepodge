from typing import Optional, Iterable, Iterator
from dataclasses import dataclass

import psutil
import hodgepodge.pattern_matching
import hodgepodge.hashing
import hodgepodge.types
import hodgepodge.files
import hodgepodge.time
import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass()
class Process:
    pid: int
    ppid: Optional[int] = None
    create_time: Optional[datetime.datetime] = None
    name: Optional[str] = None
    command_line: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None


def get_process(pid: int) -> Optional[Process]:
    p = psutil.Process(pid=pid)

    ctx = {}
    with p.oneshot():
        try:
            ctx['name'] = p.name()
            ctx['command_line'] = p.cmdline()
            ctx['ppid'] = p.ppid()
            ctx['create_time'] = hodgepodge.time.to_datetime(p.create_time())

        except (psutil.AccessDenied, psutil.ZombieProcess) as e:
            logger.info("Encountered %s while gathering process context: %s (PID: %d)", e, pid)
    return Process(pid=pid, **ctx)


def iter_processes(
        pids: Optional[Iterable[int]] = None,
        ppids: Optional[Iterable[int]] = None,
        names: Optional[Iterable[str]] = None) -> Iterator[Process]:

    #: Iterate through all processes.
    for process in psutil.process_iter():
        pid = process.pid
        ppid = process.ppid()

        #: Filter processes by PID.
        if pids and process.pid not in pids:
            continue

        #: Filter process by PPID.
        if ppids and ppid not in ppids:
            continue

        #: Lookup the process.
        process = get_process(pid)
        if not process:
            continue

        #: Filter processes by name.
        if names and process.name not in names:
            continue

        yield process

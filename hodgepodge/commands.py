from subprocess import PIPE
from hodgepodge.processes import Process

import hodgepodge.processes
import hodgepodge.types
import subprocess
import datetime
import shlex
import psutil


def execute_command(command: str) -> Process:
    args = shlex.split(command)
    p = subprocess.Popen(args, stdout=PIPE, stderr=PIPE)
    pid = p.pid

    ctx = Process(
        create_time=datetime.datetime.now(),
        pid=pid,
        command_line=' '.join(p.args),
    )
    try:
        ctx = hodgepodge.processes.get_process(pid=pid)
    except psutil.NoSuchProcess:
        pass

    stdout, stderr = p.communicate()
    ctx.stdout = hodgepodge.types.bytes_to_str(stdout)
    ctx.stderr = hodgepodge.types.bytes_to_str(stderr)
    ctx.exit_code = p.returncode
    return ctx

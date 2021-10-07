from typing import Optional

import hodgepodge
import hodgepodge.pattern_matching
import platform
import struct

WINDOWS = 'windows'
LINUX = 'linux'
DARWIN = 'darwin'

OS_TYPE = platform.system()
OS_VERSION = platform.version()


def get_os_type() -> str:
    return OS_TYPE


def get_os_version() -> str:
    return OS_VERSION


def get_os_bitness() -> int:
    return 8 * struct.calcsize("P")


def is_windows() -> bool:
    return OS_TYPE.lower() == WINDOWS


def is_linux() -> bool:
    return OS_TYPE.lower() == LINUX


def is_darwin() -> bool:
    return OS_TYPE.lower() == DARWIN


def parse_os_type(os_type: str) -> Optional[str]:
    os_type = str.lower(os_type)
    if hodgepodge.pattern_matching.str_matches_glob(os_type, patterns=[
        '*microsoft*', '*windows*', '*cygwin*', '*mingw*', '*msys*', '*dos*'
    ]):
        return WINDOWS
    elif hodgepodge.pattern_matching.str_matches_glob(os_type, patterns=[
        '*linux*', '*ubuntu*', '*rhel*', '*red*hat*', '*centos*', '*debian*', '*gentoo*', '*opensuse*', '*sles*',
    ]):
        return LINUX
    elif hodgepodge.pattern_matching.str_matches_glob(os_type, patterns=[
        '*darwin*', '*mac*os*', '*os*x*'
    ]):
        return DARWIN
    return os_type

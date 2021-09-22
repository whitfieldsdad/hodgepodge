from typing import Optional

import hodgepodge
import hodgepodge.patterns
import sys

WINDOWS = 'windows'
LINUX = 'linux'
DARWIN = 'darwin'

OS_TYPES = sorted([WINDOWS, LINUX, DARWIN])


def is_windows():
    return sys.platform == WINDOWS


def is_linux():
    return sys.platform == LINUX


def is_darwin():
    return sys.platform == DARWIN


def normalize_os_type(os_type: str) -> Optional[str]:
    os_type = str.lower(os_type)
    if hodgepodge.patterns.str_matches_glob(os_type, patterns=[
        '*microsoft*', '*windows*', '*cygwin*', '*mingw*', '*msys*', '*dos*'
    ]):
        return WINDOWS
    elif hodgepodge.patterns.str_matches_glob(os_type, patterns=[
        '*linux*', '*ubuntu*', '*rhel*', '*red*hat*', '*centos*', '*debian*', '*gentoo*', '*opensuse*', '*sles*',
    ]):
        return LINUX
    elif hodgepodge.patterns.str_matches_glob(os_type, patterns=[
        '*darwin*', '*mac*os*', '*os*x*'
    ]):
        return DARWIN
    return os_type

import string
from typing import Optional


def parse_mac_address(value: str) -> Optional[str]:
    if value:
        mac = ''.join(c for c in value if c in string.hexdigits)
        mac = ':'.join(mac[i:i + 2] for i in range(0, 12, 2)).lower()
        return mac

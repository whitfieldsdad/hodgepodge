import string


def parse_mac_address(value: str) -> str:
    mac = ''.join(c for c in value if c in string.hexdigits)
    return ':'.join(mac[i:i + 2] for i in range(0, 12, 2)).lower()

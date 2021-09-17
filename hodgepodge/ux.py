from typing import Union, Any

import arrow
import hodgepodge.time
import hodgepodge.types


def pretty_file_size(n: int) -> str:
    n = abs(n)
    for unit in '', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi':
        if n < 1000.0:
            return "%3.1f%sB" % (n, unit)
        n /= 1000.0
    return "%.1f%sB" % (n, 'Yi')


def pretty_time(timestamp: Any, include_delta: bool = False) -> str:
    if timestamp is None:
        return 'n/a'

    hint = None
    if include_delta:
        a = hodgepodge.time.get_current_time_as_epoch_time_in_fractional_seconds()
        b = timestamp
        if a != b:
            d = pretty_duration(a - b)
            if a > b:
                hint = '{} ago'.format(d)
            else:
                hint = '{} from now'.format(d)
        else:
            hint = 'just now'

    timestamp = arrow.get(timestamp).strftime("%b %e, %Y, %I:%M:%S %p")
    if hint:
        return '{} ({})'.format(timestamp, hint)
    return timestamp


def pretty_duration(seconds: Any) -> Union[str, None]:
    parts = []
    years, days, hours, minutes, seconds = hodgepodge.time.convert_time_to_parts(seconds)
    for unit, value in [
        ('year', years),
        ('day', days),
        ('hour', hours),
        ('minute', minutes),
        ('second', seconds),
    ]:
        if value:
            part = '{} {}'.format(value, pluralize(unit) if value > 1 else unit)
            parts.append(part)
    return join_with_oxford_comma(parts)


def pluralize(value: str) -> str:
    if not value.endswith("s"):
        value += "s"
    return value


def remove_suffix(value: str, suffix: str) -> str:
    if value.endswith(suffix):
        value = value[:-len(suffix)]
    return value


def join_with_oxford_comma(args) -> str:
    if hodgepodge.types.is_iterator(args):
        args = list(args)

    n = len(args)
    if n:
        if n == 1:
            return args.pop()
        elif n == 2:
            return ' and '.join(args)
        else:
            last = args.pop()
            return '{}, and {}'.format(', '.join(args), last)
    return ''

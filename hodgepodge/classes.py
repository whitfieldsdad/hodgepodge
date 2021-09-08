from typing import Any, Dict, Callable


def get_attributes(obj: Any, ignore_hidden: bool = True) -> Dict[str, Any]:
    attrs = dict([(attr, getattr(obj, attr)) for attr in dir(obj)])
    if ignore_hidden:
        attrs = dict((k, v) for (k, v) in attrs.items() if k.startswith('_') is False)
    return attrs


def get_functions(obj: Any, ignore_hidden: bool = True) -> Dict[str, Callable[[Any], Any]]:
    attrs = get_attributes(obj=obj, ignore_hidden=ignore_hidden)
    return dict((k, v) for (k, v) in attrs.items() if callable(v) is True)


def get_variables(obj: Any, ignore_hidden: bool = True) -> Dict[str, Callable[[Any], Any]]:
    attrs = get_attributes(obj=obj, ignore_hidden=ignore_hidden)
    return dict((k, v) for (k, v) in attrs.items() if callable(v) is False)

import os
import copy
import collections
import yaml

DEFAULTS = {
    # https://docs.python.org/3.3/library/string.html#formatspec
    "filter": "status:pending",
    "columns": ["id", "project", "description"],
    "bindings": {
        "j": "down",
        "down": "down",
        "k": "up",
        "up": "up",
        "g": "jump_top",
        "home": "jump_top",
        "G": "jump_bottom",
        "end": "jump_bottom",
        ":": "command",
    }
}


def deep_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def load(path):
    # FIXME use some central configuration directory
    if os.path.exists(path):
        with open(path) as f:
            overrides = (yaml.load(f) or {})
    else:
        overrides = {}
    conf = copy.deepcopy(DEFAULTS)
    return deep_update(conf, overrides)

__all__ = ["load"]

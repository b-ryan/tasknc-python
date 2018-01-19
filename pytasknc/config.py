import copy
import collections
import yaml

DEFAULTS = {
    # https://docs.python.org/3.3/library/string.html#formatspec
    "task_format": "{id:<3} {description}",
    "bindings": {
        "j": "down",
        "k": "up",
    }
}


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def load(path):
    with open(path) as f:
        overrides = (yaml.load(f) or {})
    conf = copy.deepcopy(DEFAULTS)
    return update(conf, overrides)

__all__ = ["load"]

import copy
import yaml

DEFAULTS = {
    "bindings": {
        "j": "down",
        "k": "up",
    }
}


def load(path):
    with open(path) as f:
        overrides = yaml.load(f)
    conf = copy.deepcopy(DEFAULTS)
    if overrides:
        conf["bindings"].update(overrides.get("bindings", {}))
    return conf

__all__ = ["load"]

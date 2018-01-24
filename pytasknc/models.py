from collections import namedtuple

TaskWindow = namedtuple("TaskWindow", ["offset", "limit", "selected"])
State = namedtuple("State", ["tasks", "selected", "status_msg", "page_offset",
                             "page_limit", "width", "height", "col_widths"])


def update(state, updates):
    kwargs = state._asdict()
    kwargs.update(updates)
    return State(**kwargs)

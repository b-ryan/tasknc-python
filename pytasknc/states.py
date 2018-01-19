from functools import wraps
from collections import namedtuple

State = namedtuple("State", ["tasks", "selected", "status_msg", "max_tasks"])


def update_state(state, updates):
    kwargs = state._asdict()
    kwargs.update(updates)
    return State(**kwargs)


def _action(*, clear_status_msg=True):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(conf, state):
            updates = (fn(conf, state) or {})
            if clear_status_msg and "status_msg" not in updates:
                updates["status_msg"] = ""
            return update_state(state, updates)
        return wrapped
    return wrapper


@_action()
def no_action(conf, state):
    pass


@_action()
def up(conf, state: State):
    if state.selected == 0:
        return {"status_msg": "already at top"}
    else:
        return {"selected": state.selected - 1}


@_action()
def down(conf, state: State):
    if state.selected == state.max_tasks - 1:
        return {"status_msg": "already at bottom"}
    else:
        return {"selected": state.selected + 1}

ACTIONS = {
    "up": up,
    "down": down,
}


def get_action(name):
    """Returns an action function, which is a function that accepts a config
    and a state and returns a dict of things to change in the state."""
    return ACTIONS.get(name, no_action)

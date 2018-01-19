from functools import wraps
from .common import update_state, State


def _action(*, clear_status_msg=True):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(conf, state):
            updates = fn(conf, state)
            if clear_status_msg and "status_msg" not in updates:
                updates["status_msg"] = ""
            if updates:
                return update_state(state, **updates)
            return state
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


def get(name):
    """Returns a function that accepts config and a state. Returns a new
    state."""
    return ACTIONS.get(name, no_action)

__all__ = ["get"]

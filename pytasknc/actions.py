from functools import wraps
from . import models


def _action(*, clear_status_msg=True):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(conf, state):
            updates = (fn(conf, state) or {})
            if clear_status_msg and "status_msg" not in updates:
                updates["status_msg"] = ""
            return models.update(state, updates)
        return wrapped
    return wrapper


@_action()
def no_action(conf, state):
    pass


@_action()
def up(conf, state: models.State):
    if state.selected == 0:
        return {"status_msg": "already at top"}
    new_idx = state.selected - 1
    if new_idx < state.page_offset:
        return {"selected": new_idx, "page_offset": state.page_offset - 1}
    else:
        return {"selected": new_idx}


@_action()
def down(conf, state: models.State):
    if state.selected == len(state.tasks) - 1:
        return {"status_msg": "already at bottom"}
    new_idx = state.selected + 1
    if new_idx >= (state.page_offset + state.page_limit):
        return {"selected": new_idx, "page_offset": state.page_offset + 1}
    else:
        return {"selected": new_idx}


@_action()
def jump_top(conf, state: models.State):
    if state.selected == 0:
        return {"status_msg": "already at top"}
    return {"selected": 0, "page_offset": 0}


@_action()
def jump_bottom(conf, state: models.State):
    max_idx = len(state.tasks) - 1
    if state.selected == max_idx:
        return {"status_msg": "already at bottom"}
    return {"selected": max_idx,
            "page_offset": max(0, max_idx - state.page_limit + 1)}

ACTIONS = {
    "up": up,
    "down": down,
    "jump_top": jump_top,
    "jump_bottom": jump_bottom,
}


def get_action(name):
    """Returns an action function, which is a function that accepts a config
    and a state and returns a dict of things to change in the state."""
    return ACTIONS.get(name, no_action)

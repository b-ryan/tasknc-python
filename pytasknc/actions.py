import logging
from functools import wraps
from . import models, taskw, draw, grid
from .models import update

# pylint: disable=unused-argument

logger = logging.getLogger(__name__)


def _action(*, clear_status_msg=True):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(conf, state, screen, *args, **kwargs):
            updates = (fn(conf, state, screen, *args, **kwargs) or {})
            if clear_status_msg and "status_msg" not in updates:
                updates["status_msg"] = ""
            if "page" in updates:
                updates["page"] = update(state.page, **updates["page"])
            return update(state, **updates)
        return wrapped
    return wrapper


@_action()
def no_action(conf, state, screen):
    pass


@_action()
def up(conf, state: models.State, screen):
    if state.selected == 0:
        return {"status_msg": "already at top"}
    new_idx = state.selected - 1
    if new_idx < state.page.offset:
        return {"selected": new_idx, "page": {"offset": state.page.offset - 1}}
    return {"selected": new_idx}


@_action()
def down(conf, state: models.State, screen):
    if state.selected == len(state.tasks) - 1:
        return {"status_msg": "already at bottom"}
    new_idx = state.selected + 1
    if new_idx >= (state.page.offset + state.page.limit):
        return {"selected": new_idx, "page": {"offset": state.page.offset + 1}}
    return {"selected": new_idx}


@_action()
def jump_top(conf, state: models.State, screen):
    if state.selected == 0:
        return {"status_msg": "already at top"}
    return {"selected": 0, "page": {"offset": 0}}


@_action()
def jump_bottom(conf, state: models.State, screen):
    max_idx = len(state.tasks) - 1
    if state.selected == max_idx:
        return {"status_msg": "already at bottom"}
    return {
        "selected": max_idx,
        "page":{"offset": max(0, max_idx - state.page.limit + 1)},
    }


@_action(clear_status_msg=False)
def resize(conf, state: models.State, screen):
    height, width = screen.getmaxyx()
    new_page_limit = height - draw.NUM_NON_TASK_LINES
    return {
        "width": width,
        "height": height,
        "page": {
            # The selected item may be too far down after the resize. If it is,
            # then move the offset to where the selected item can be seen
            "offset": max(state.page.offset,
                          (state.selected - new_page_limit + 1)),
            "limit": new_page_limit,
        },
        "col_widths": grid.get_col_widths(conf, state.tasks, screen),
    }


@_action()
def command(conf, state: models.State, screen):
    return {
        "mode": "input",
        "status_msg": ":",
    }

ACTIONS = {
    "up": up,
    "down": down,
    "jump_top": jump_top,
    "jump_bottom": jump_bottom,
    "resize": resize,
    "command": command,
}


def get_action(name):
    """Returns an action function, which is a function that accepts a config
    and a state and returns a dict of things to change in the state."""
    return ACTIONS.get(name, no_action)


@_action()
def handle_input(conf, state, screen, response: bytes):
    logger.debug("response %s", response)
    return {
        "mode": "execute",
        "execute_command": response.decode("utf-8"),
    }


@_action()
def handle_execute(conf, state, screen):
    logger.debug("executing")
    taskw.execute(state.execute_command)
    return {
        "mode": "normal",
        "execute_command": None,
        "tasks": taskw.export(conf["filter"]),
    }

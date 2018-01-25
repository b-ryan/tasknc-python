#!/usr/bin/env python
import curses
import logging
from . import taskw, models, actions, config, draw, grid

logging.basicConfig(filename="debug.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def init_state(conf, screen):
    tasks = taskw.export(conf["filter"])
    height, width = screen.getmaxyx()
    return models.State(
        tasks,
        status_msg="",
        width=width,
        height=height,
        selected=0,
        page=models.Page(
            offset=0,
            limit=(height - draw.NUM_NON_TASK_LINES),
        ),
        col_widths=grid.get_col_widths(conf, tasks, screen),
    )


SPECIAL_KEYS = {
    49: "home",
    52: "end",
    65: "up",
    66: "down",
    curses.KEY_RESIZE: "resize",
}
# forced actions are things that are not configurable by the user and generally
# do not actually correspond to a key press. Instead, they might be the
# resizing of the screen, which curses communicates to our code as if it were a
# key press.
FORCED_ACTIONS = {
    "resize",
}


def main():
    conf = config.load("config.yml")
    try:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        state = init_state(conf, screen)
        draw.draw_full(conf, state, screen)
        while screen:
            x = screen.getch()
            key_name = SPECIAL_KEYS.get(x) or chr(x)
            action_name = key_name if key_name in FORCED_ACTIONS \
                else conf["bindings"].get(key_name)
            logger.debug("key press %s, key_name %s, action name %s",
                         x, key_name, action_name)
            action_fn = actions.get_action(action_name)
            new_state = action_fn(conf, state, screen)
            draw.draw_diff(conf, state, new_state, screen)
            state = new_state
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

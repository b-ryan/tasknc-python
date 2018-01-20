#!/usr/bin/env python
import curses
import logging
from . import common, states, config, draw

logging.basicConfig(filename="debug.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)
MIN_DESC_WIDTH = 5


def column_max_widths(conf, tasks):
    maxes = {k: 0 for k in conf["columns"]}
    for task in tasks:
        for col in conf["columns"]:
            maxes[col] = max(maxes[col], len(str(task.get(col) or "")))
    return maxes


def column_trimmed_widths(col_widths, total_width):
    if "description" not in col_widths:
        return col_widths
    non_desc_width = 0
    for col, width in col_widths.items():
        if col != "description":
            non_desc_width += width
    num_spaces = len(col_widths) - 1
    desc_width = max(MIN_DESC_WIDTH, total_width - non_desc_width - num_spaces)
    col_widths["description"] = desc_width
    return col_widths


def get_col_widths(conf, tasks, screen):
    maxes = column_max_widths(conf, tasks)
    _, total_width = screen.getmaxyx()
    return column_trimmed_widths(maxes, total_width)


def init_state(conf, screen):
    tasks = common.task_export(conf["filter"])
    height, width = screen.getmaxyx()
    return states.State(tasks, selected=0, status_msg="", page_offset=0,
                        page_limit=(height - draw.NUM_NON_TASK_LINES),
                        width=width, height=height,
                        col_widths=get_col_widths(conf, tasks, screen))

SPECIAL_KEYS = {
    49: "home",
    52: "end",
    65: "up",
    66: "down",
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
            logger.debug("key press %s", x)
            key_name = SPECIAL_KEYS.get(x) or chr(x)
            action_name = conf["bindings"].get(key_name)
            action_fn = states.get_action(action_name)
            new_state = action_fn(conf, state)
            draw.draw_diff(conf, state, new_state, screen)
            state = new_state
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

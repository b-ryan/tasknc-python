#!/usr/bin/env python
import curses
from . import common, actions, config
from .config import load


def main():
    x = 0
    conf = config.load("config.yml")
    state = common.NcursesState(conf)
    try:
        while x != ord("4"):
            screen = curses.initscr()
            screen.clear()
            title_fmt = ""
            screen.addstr(0, 0, title_fmt)
            fmt = "{id} {description}"
            for idx, task in enumerate(state.tasks):
                if idx == state.selected:
                    text_attr = curses.A_STANDOUT
                else:
                    text_attr = 0
                screen.addstr(1 + idx, 0, fmt.format(**task), text_attr)
            screen.refresh()
            x = screen.getch()
            action_name = state.conf["bindings"].get(chr(x))
            action_fn = actions.get(action_name)
            action_fn(state)
            curses.endwin()
    finally:
        curses.endwin()

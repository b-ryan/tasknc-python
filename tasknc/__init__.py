#!/usr/bin/env python
import curses
from . import common, actions, config
from .config import load


def draw(conf, state, screen):
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
    curses.curs_set(0)
    screen.refresh()


def main():
    conf = config.load("config.yml")
    state = common.init_state(conf)
    try:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        draw(conf, state, screen)
        while screen:
            x = screen.getch()
            action_name = conf["bindings"].get(chr(x))
            action_fn = actions.get(action_name)
            new_state = action_fn(conf, state)
            if state != new_state:
                draw(conf, new_state, screen)
                state = new_state
    finally:
        curses.endwin()

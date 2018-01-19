#!/usr/bin/env python
import curses
from . import common, states, config, draw


def init_state(conf, screen):
    tasks = common.task_export(conf["filter"])
    height, width = screen.getmaxyx()
    return states.State(tasks, selected=0, status_msg="", page_offset=0,
                        page_limit=(height - 2), width=width, height=height)


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
            action_name = conf["bindings"].get(chr(x))
            action_fn = states.get_action(action_name)
            new_state = action_fn(conf, state)
            draw.draw_diff(conf, state, new_state, screen)
            state = new_state
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

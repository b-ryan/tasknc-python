#!/usr/bin/env python
import curses
from . import common, actions, config


def draw(conf, state, screen):
    screen.clear()
    height, width = screen.getmaxyx()
    title_fmt = ""
    screen.addstr(0, 0, title_fmt)
    fmt = conf["task_format"]
    max_tasks = height - 2
    for idx, task in enumerate(state.tasks[:max_tasks]):
        if idx == state.selected:
            text_attr = curses.A_STANDOUT
        else:
            text_attr = 0
        text = fmt.format(**task)[:width]
        text += (" " * (width - len(text)))
        screen.addstr(1 + idx, 0, text, text_attr)
    screen.addstr(height - 1, 0, state.status_msg)
    curses.curs_set(0)
    screen.refresh()


def init_state(conf, screen):
    height, _ = screen.getmaxyx()
    tasks = common.task_export(conf["filter"])
    return common.State(tasks, selected=0, status_msg="",
                        max_tasks=(height - 2))


def main():
    conf = config.load("config.yml")
    try:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        state = init_state(conf, screen)
        draw(conf, state, screen)
        while screen:
            x = screen.getch()
            action_name = conf["bindings"].get(chr(x))
            action_fn = actions.get(action_name)
            new_state = action_fn(conf, state)
            if state != new_state:
                draw(conf, new_state, screen)
                state = new_state
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

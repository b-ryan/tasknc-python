import curses
from .states import State


def fmt_task(conf, task, screen):
    fmt = conf["task_format"]
    _, width = screen.getmaxyx()
    text = fmt.format(**task)[:width]
    text += (" " * (width - len(text)))
    return text


def change_highlight(conf, old_state, new_state, screen):
    old_task = old_state.tasks[old_state.selected]
    screen.addstr(1 + old_state.selected, 0, fmt_task(conf, old_task, screen))
    new_task = new_state.tasks[new_state.selected]
    screen.addstr(1 + new_state.selected, 0, fmt_task(conf, new_task, screen),
                  curses.A_STANDOUT)


def full_draw(conf, state, screen):
    screen.clear()
    height, _ = screen.getmaxyx()
    title_fmt = ""
    screen.addstr(0, 0, title_fmt)
    max_tasks = height - 2
    for idx, task in enumerate(state.tasks[:max_tasks]):
        if idx == state.selected:
            text_attr = curses.A_STANDOUT
        else:
            text_attr = 0
        text = fmt_task(conf, task, screen)
        screen.addstr(1 + idx, 0, text, text_attr)
    screen.addstr(height - 1, 0, state.status_msg)
    curses.curs_set(0)
    screen.refresh()


def draw_state_updates(conf, old_state, new_state, screen):
    if old_state.selected != new_state.selected:
        change_highlight(conf, old_state, new_state, screen)

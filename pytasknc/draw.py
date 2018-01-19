import curses
from .states import State


def create_screen_lines(conf, state, height):
    lines = ["" for _ in range(height)]
    lines[0] = " "  # FIXME put a title in there
    for idx, task in enumerate(state.tasks[:(height - 2)]):
        text_attr = curses.A_STANDOUT if idx == state.selected else 0
        lines[1 + idx] = (conf["task_format"].format(**task), text_attr)
    lines[-1] = state.status_msg
    return lines


def draw_diff(conf, old_state, new_state, screen):
    height, width = screen.getmaxyx()
    old_lines = create_screen_lines(conf, old_state, height)
    new_lines = create_screen_lines(conf, new_state, height)
    for idx, line in enumerate(new_lines):
        if line == old_lines[idx]:
            continue
        if isinstance(line, tuple):
            line, text_attr = line
        else:
            text_attr = 0
        trimmed = line[:width]
        padded = trimmed + (" " * (width - len(trimmed) - 1))
        screen.addstr(idx, 0, padded, text_attr)
    curses.curs_set(0)


def draw_full(conf, state, screen):
    old_state = State([], 0, "", 0)
    draw_diff(conf, old_state, state, screen)

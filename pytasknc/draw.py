import curses
from .states import State


def create_lines(conf, state: State):
    lines = ["" for _ in range(state.height)]
    lines[0] = " "  # FIXME put a title in there
    for view_idx in range(state.page_limit):
        task_idx = view_idx + state.page_offset
        if task_idx >= len(state.tasks):
            break
        task = state.tasks[task_idx]
        text_attr = curses.A_STANDOUT if task_idx == state.selected else 0
        lines[1 + view_idx] = (conf["task_format"].format(**task), text_attr)
    lines[-1] = state.status_msg
    return lines


def draw_diff(conf, old_state, new_state, screen):
    old_lines = create_lines(conf, old_state) if old_state else []
    new_lines = create_lines(conf, new_state)
    for idx, line in enumerate(new_lines):
        if old_lines and line == old_lines[idx]:
            continue
        if isinstance(line, tuple):
            line, text_attr = line
        else:
            text_attr = 0
        trimmed = line[:new_state.width]
        padded = trimmed + (" " * (new_state.width - len(trimmed) - 1))
        screen.addstr(idx, 0, padded, text_attr)
    curses.curs_set(0)


def draw_full(conf, state, screen):
    draw_diff(conf, None, state, screen)

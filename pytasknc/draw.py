import curses
import logging
from .models import State

logger = logging.getLogger(__name__)
NUM_NON_TASK_LINES = 2


class _fmt_dict(dict):
    def __missing__(self, key):
        return ""


def format_row(conf, state, row):
    items = []
    for idx, col in enumerate(conf["columns"]):
        width = state.col_widths[col]
        fmt = "{:<" + str(width) + "}"
        items.append(fmt.format(row[idx]))
    return " ".join(items)


def format_header(conf, state):
    return format_row(conf, state, conf["columns"])


def format_task(conf, state, task):
    row = [task.get(col) or "" for col in conf["columns"]]
    return format_row(conf, state, row)


def create_lines(conf, state: State):
    lines = ["" for _ in range(state.height)]
    lines[0] = (format_header(conf, state), curses.A_BOLD)
    for view_idx in range(state.page.limit):
        task_idx = view_idx + state.page.offset
        if task_idx >= len(state.tasks):
            break
        task = _fmt_dict(state.tasks[task_idx])
        text_attr = curses.A_STANDOUT if task_idx == state.selected else 0
        lines[1 + view_idx] = (format_task(conf, state, task), text_attr)
    lines[-1] = state.status_msg
    return lines


def draw(conf, state, screen, old_state=None):
    old_lines = create_lines(conf, old_state) if old_state else []
    new_lines = create_lines(conf, state)
    for idx, line in enumerate(new_lines):
        if len(old_lines) > idx and line == old_lines[idx]:
            continue
        if isinstance(line, tuple):
            line, text_attr = line
        else:
            text_attr = 0
        trimmed = line[:state.width]
        padded = trimmed + (" " * (state.width - len(trimmed) - 1))
        screen.addstr(idx, 0, padded, text_attr)
    curses.curs_set(0)

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

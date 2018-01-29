from collections import namedtuple

Page = namedtuple("Page", ["offset", "limit"])
State = namedtuple("State", ["tasks", "status_msg", "width", "height",
                             "col_widths", "selected", "page", "mode",
                             "execute_command"])


def update(model, **kwargs):
    new_kwargs = model._asdict()
    new_kwargs.update(kwargs)
    return model.__class__(**new_kwargs)

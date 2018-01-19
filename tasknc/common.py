from subprocess import Popen, PIPE
from collections import namedtuple
import json


def task_export(*task_filters):
    cmd = ["task", "export"] + list(task_filters)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        # TODO show some warning or something
        return []
    return json.loads(stdout.decode("utf-8"))

State = namedtuple("State", ["tasks", "selected", "status_msg"])


def init_state(conf):
    return State(task_export("status:pending"), 0, None)


def update_state(state, **updates):
    kwargs = state._asdict()
    kwargs.update(updates)
    return State(**kwargs)

__all__ = ["State", "init_state", "update_state"]

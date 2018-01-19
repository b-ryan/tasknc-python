from subprocess import Popen, PIPE
import json


def task_export(*task_filters):
    cmd = ["task", "export"] + list(task_filters)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        # TODO show some warning or something
        return []
    return json.loads(stdout.decode("utf-8"))


class NcursesState(object):
    def __init__(self, conf):
        self.conf = conf
        self.selected = 0
        self.tasks = []
        self.refresh_tasks()

    def refresh_tasks(self):
        self.tasks = task_export("status:pending")

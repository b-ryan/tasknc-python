from subprocess import Popen, PIPE
import json


def export(task_filters: str):
    cmd = ["task", "export"] + task_filters.split()
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        # TODO show some warning or something
        return []
    return json.loads(stdout.decode("utf-8"))

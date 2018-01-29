from subprocess import Popen, PIPE
import json
import shlex
import logging

logger = logging.getLogger(__name__)


def export(task_filters: str):
    cmd = ["task", "export"] + task_filters.split()
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        logger.error("%s || %s", stdout, stderr)
        # TODO show some warning or something
        return []
    return json.loads(stdout.decode("utf-8"))


def execute(command: str):
    args = shlex.split(command)
    if not args:
        return
    Popen(["task"] + args).wait()
    input("Press enter to continue")

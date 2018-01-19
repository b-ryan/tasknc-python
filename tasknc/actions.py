from .common import NcursesState


def no_action(state):
    pass


def up(state: NcursesState):
    if state.selected == 0:
        # TODO warn that they're already there
        pass
    else:
        state.selected -= 1


def down(state: NcursesState):
    if state.selected == len(state.tasks) - 1:
        # TODO warn that they're already there
        pass
    else:
        state.selected += 1

ACTIONS = {
    "up": up,
    "down": down,
}


def get(name):
    """Returns a function that accepts an NcursesState object and updates the
    state."""
    return ACTIONS.get(name, no_action)

__all__ = ["get", "DEFAULT_BINDINGS"]

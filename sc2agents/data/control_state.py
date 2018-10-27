"""A random agent for starcraft."""

SCOUT_GROUP = 1
MAIN_GROUP = 6


class ControlState:

    def __init__(self):
        self.army_selected = False

        self.current_scout_target = None
        self.current_scout_list = None

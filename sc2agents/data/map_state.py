"""A random agent for starcraft."""


class MapState:

    def __init__(self, minimap_size):

        self.current_loc = None
        self.current_main_base_loc = None

        self.minimap_size = minimap_size

    def centered_at_base(self):
        return self.current_loc \
               and self.current_loc == self.current_main_base_loc

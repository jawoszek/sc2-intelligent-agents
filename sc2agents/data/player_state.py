"""A random agent for starcraft."""
from sc2agents.data.building_state import BuildingState
from sc2agents.data.control_state import ControlState
from sc2agents.data.map_state import MapState


class PlayerState:

    def __init__(self,
                 building_state: BuildingState,
                 control_state: ControlState,
                 map_state: MapState):
        self.building_state = building_state
        self.control_state = control_state
        self.map_state = map_state

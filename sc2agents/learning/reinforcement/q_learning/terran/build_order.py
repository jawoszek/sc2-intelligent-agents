"""A random agent for starcraft."""
from pysc2.lib import units

from sc2agents.data.building_state import BuildingState
from sc2agents.learning.reinforcement.q_learning.table import Table
from copy import deepcopy
from random import choice


def recruit_order_pos_to_str(recruit_order):
    return map(lambda unit: str(unit.value), recruit_order)


def state_to_str(state: BuildingState):
    return str(state.already_recruit) + ',' + str(state.already_built)


class BuildOrder:

    def __init__(self, building_q_table: Table, recruit_q_table: Table):
        self.building_q_table = building_q_table
        self.recruit_q_table = recruit_q_table
        self.previous_state = None
        self.previous_recruit_state = None
        self.next_building = None
        self.next_recruit = None
        self.marines = 0

    def build_order_reached(self, _, state: BuildingState):
        built = self.get_built_building(state, self.previous_state)
        if built:
            c_state = state_to_str(self.previous_state)
            q_state = state_to_str(state)
            self.building_q_table.learn(c_state, built, 1 if built is not None else 0, q_state)
        self.next_building = self.building_q_table.choose_action(state_to_str(state))
        self.previous_state = deepcopy(state)
        return self.next_building

    def build_order_building(self, _1, _2=None):
        return self.next_building

    def recruit_order_finished(self, state: BuildingState):
        recruited = self.get_recruited_unit(state, self.previous_state)
        self.marines = max(state.already_recruit.get(units.Terran.Marine, 0), self.marines)
        if recruited:
            c_state = state_to_str(self.previous_recruit_state)
            q_state = state_to_str(state)
            self.recruit_q_table.learn(c_state, recruited,
                                       1 if recruited is units.Terran.Marine else -1,
                                       q_state)
        self.next_recruit = self.recruit_q_table.choose_action(
            state_to_str(state))
        self.previous_recruit_state = deepcopy(state)
        return not self.next_recruit

    def recruit_order_next(self, _: BuildingState):
        return self.next_recruit

    def state_with_unit(self, state: BuildingState, unit):
        if unit is None:
            return state
        copied = deepcopy(state)
        copied.already_recruit[unit] = copied.already_recruit.get(unit, 0) + 1
        return copied

    def state_with_building(self, state: BuildingState, buiding):
        if buiding is None:
            return state
        copied = deepcopy(state)
        copied.already_built[buiding] = copied.already_built.get(buiding, 0) + 1
        return copied

    def get_recruited_unit(self, state, prev_state):
        if prev_state is None or state is None:
            return None
        vals = list()
        for unit, count in state.already_recruit.items():
            if prev_state.already_recruit.get(unit, 0) < count:
                vals.append(unit)
        if vals:
            return choice(vals)
        return None

    def get_built_building(self, state, prev_state):
        if prev_state is None or state is None:
            return None
        vals = list()
        for b, count in state.already_built.items():
            if prev_state.already_built.get(b, 0) < count:
                vals.append(b)
        if vals:
            return choice(vals)
        return None

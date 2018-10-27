"""A random agent for starcraft."""
from sc2agents.data.building_state import BuildingState


def recruit_order_pos_to_str(recruit_order):
    return map(lambda unit: str(unit.value), recruit_order)


class BuildOrder:

    def __init__(self, recruit_order, build_order):
        self.recruit_order = recruit_order
        self.build_order = build_order

    def build_order_reached(self, food_used, state: BuildingState):
        return state.build_order_pos < len(self.build_order) \
               and \
               food_used >= self.build_order[state.build_order_pos][0]

    def build_order_building(self, state: BuildingState, index=None):
        if index is None:
            index = state.build_order_pos

        if index >= len(self.build_order):
            return None

        return self.build_order[index][1]

    def recruit_order_finished(self, state: BuildingState):
        return state.recruit_order_pos >= len(self.recruit_order)

    def recruit_order_next(self, state: BuildingState):
        return self.recruit_order[state.recruit_order_pos]

    def storage_format(self):
        build_order_part = self.build_order_storage_format()
        recruit_order_part = self.recruit_order_storage_format()
        return "{0},{1}".format(build_order_part, recruit_order_part)

    def build_order_storage_format(self):
        build_order_listed = [
            "({0},{1})".format(pop, building)
            for pop, building in self.build_order
        ]
        return "[{0}]".format(','.join(build_order_listed))

    def recruit_order_storage_format(self):
        recruit_order_listed = ','.join(
            recruit_order_pos_to_str(self.recruit_order))
        return '[{0}]'.format(recruit_order_listed)

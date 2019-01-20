"""A random agent for starcraft."""
from pysc2.lib import actions, units

import sc2agents.data.terran.constants as terran_constants
from sc2agents.data.parameters import Parameters
from sc2agents.data.player_state import PlayerState
from sc2agents.stages.stage import Stage

FUNCTIONS = actions.FUNCTIONS


def recruitment_building(unit):
    return terran_constants.UNIT_TO_BUILDING[unit]


def units_recruited_at(building_type):
    return [
        unit for (unit, building)
        in terran_constants.UNIT_TO_BUILDING.items()
        if building == building_type
    ]


def unit_cost(unit_type):
    return terran_constants.UNIT_TO_COST.get(unit_type, 0)


def unit_to_actions(unit_type):
    return terran_constants.UNIT_TO_ACTION[unit_type]


class TerranRecruitStage(Stage):

    def __init__(self,
                 parameters: Parameters,
                 player_state: PlayerState):

        super().__init__(2, parameters, player_state)
        self.currently_recruiting = None
        self.army_selected = False

    def process(self, obs):
        super(TerranRecruitStage, self).process(obs)
        scv = units.Terran.SCV
        map_state = self.player_state.map_state
        building_state = self.player_state.building_state

        if not map_state.centered_at_base():
            self.move_screen_to_cc()
            return

        if not self.parameters.recruit_order_finished(building_state):
            unit_to_recruit = self.parameters.recruit_order_next(
                building_state)
            if self.recruit(unit_to_recruit):
                self.remaining_executions -= 1
            return

        already_recruited_scv = building_state.already_recruit[scv]
        if self.obs.player.food_workers < already_recruited_scv:
            if self.recruit(scv, replacement=True):
                self.remaining_executions -= 1
            return

        army_count = building_state.already_recruited_army_units()
        if army_count > self.obs.player.army_count:
            if self.currently_recruiting is None and not self.army_selected \
                    and self.obs.can_select_army():
                self.select_army()
                self.army_selected = True
                return

            missing_units = self.missing_army_units()
            if missing_units:
                unit_to_recruit = list(missing_units.items())[0][0]
                if self.recruit(unit_to_recruit, replacement=True):
                    self.remaining_executions -= 1
                return

        self.remaining_executions -= 1
        return

    def recruit(self, unit_to_recruit, replacement=False):
        self.currently_recruiting = unit_to_recruit
        building_state = self.player_state.building_state
        building_to_use = recruitment_building(unit_to_recruit)
        all_units_to_check_in_queue = units_recruited_at(building_to_use)
        count_of_buildings_to_use = self.obs.count_units_on_screen(
            building_to_use)

        if unit_cost(unit_to_recruit) > self.obs.player.minerals:
            self.currently_recruiting = None
            return True

        if count_of_buildings_to_use < 1:
            if not replacement:
                building_state.recruit_order_pos += 1
            self.currently_recruiting = None
            return True

        already_recruiting = self.units_in_queue(all_units_to_check_in_queue)

        if already_recruiting > 3 * count_of_buildings_to_use:
            self.currently_recruiting = None
            return True

        if not self.obs.unit_type_selected(building_to_use):
            self.select_units(building_to_use)
            self.army_selected = False
            return False

        action = unit_to_actions(unit_to_recruit)

        if action.id not in self.obs.obs.available_actions:
            # TODO proper logging
            print("Unit {0} can't be recruited".format(unit_to_recruit))
            self.currently_recruiting = None
            return True

        self.queue.append(action('now'))
        if not replacement:
            building_state.recruit_order_pos += 1
            building_state.add_unit(unit_to_recruit, 1)
        self.currently_recruiting = None
        return False

    def missing_army_units(self):
        building_state = self.player_state.building_state
        selected_units = self.selected_units_count()
        missing_units = {}
        for unit, count in building_state.already_recruit.items():
            if unit is units.Terran.SCV:
                continue
            missing_count = count - selected_units.get(unit, 0)
            if missing_count > 0:
                missing_units[unit] = missing_count
        return missing_units

    def selected_units_count(self):
        selected = self.get_selected_units()
        selected_units = {}
        # TODO refactor to dict comprehension
        for unit in selected:
            new_value = selected_units.get(unit.unit_type, 0) + 1
            selected_units[unit.unit_type] = new_value
        return selected_units

    def get_selected_units(self):
        single_select = self.obs.obs.single_select
        multi_select = self.obs.obs.multi_select
        return single_select if single_select.any() else multi_select

    def units_in_queue(self, unit_types):
        return len([
            unit for unit
            in self.obs.obs.build_queue
            if unit.unit_type in unit_types
        ])

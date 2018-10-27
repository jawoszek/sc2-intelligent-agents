"""A random agent for starcraft."""
import random
from pysc2.lib import actions, units
from pysc2.lib.point import Point
from sc2agents.stages.stage import Stage
from sc2agents.data.player_state import PlayerState
from sc2agents.data.parameters import Parameters
import sc2agents.data.terran.constants as terran_constants


FUNCTIONS = actions.FUNCTIONS


def building_action(building):
    return terran_constants.BUILDING_TO_ACTION[building]


def buildings_requirements():
    return terran_constants.BUILDING_TO_REQUIREMENTS


def building_cost(building):
    return terran_constants.BUILDING_TO_COST.get(building, 0)


def building_cost_vespene(building):
    return terran_constants.BUILDING_TO_COST_VESPENE.get(building, 0)


def labs():
    return terran_constants.LAB_TO_BUILDING


def unit_is_idle_worker(unit):
    return unit.unit_type == units.Terran.SCV


# TODO proper logging
class TerranBuildStage(Stage):

    def __init__(self,
                 parameters: Parameters,
                 player_state: PlayerState):
        super().__init__(3, parameters, player_state)
        self.steps_since_ordered_building = None
        self.count_of_building_during_order = None
        self.idle_workers_on_order = None
        self.worker_chosen = False
        self.worker_moved = False
        self.lab_buildings_chosen = False
        self.queue_cleared_for_lab = False
        self.failed_attempts = 0

    def process(self, obs):
        super(TerranBuildStage, self).process(obs)
        building_state = self.player_state.building_state

        if not self.player_state.map_state.centered_at_base():
            self.move_screen_to_cc()
            return

        if self.player_state.building_state.currently_building:
            # TODO enable after new pysc2 release
            # if not self.worker_moved and self.idle_workers_on_order
            # <= self.count_idle_workers_on_screen(obs):
            #     print('Worker not started building')
            #     self.remaining_actions -= 1
            #     self.reset_stage()
            #     return
            # self.worker_moved = True
            if self.steps_since_ordered_building is not None:
                currently_building = building_state.currently_building
                if self.obs.count_units_on_screen(currently_building, False) \
                        > self.count_of_building_during_order:
                    print('Built successfully')
                    building_state.build_order_pos += 1
                    building_state.add_building(currently_building)
                    self.reset_stage()
                    self.remaining_executions -= 1
                    return

                if self.steps_since_ordered_building > 20:
                    print('Abandoned due to timeout')
                    self.reset_stage()
                    self.remaining_executions -= 1
                    return

                self.steps_since_ordered_building += 1
                return
            self.reset_stage()
            self.remaining_executions -= 1
            return

        if self.next_build_order_reached():
            should_pass_action = self.order_building(
                self.parameters.build_order_building(building_state))
            if should_pass_action:
                self.remaining_executions -= 1
            return

        self.remaining_executions -= 1
        return

    def next_build_order_reached(self):
        return self.parameters.build_order_reached(
            self.obs.player.food_used, self.player_state.building_state)

    def previous_building_built(self):
        building_state = self.player_state.building_state

        if building_state.build_order_pos < 1:
            return True

        previous_building = self.parameters.build_order_building(
            building_state, building_state.build_order_pos - 1)
        return self.obs.count_units_on_screen(previous_building) > 0

    def order_building(self, building):
        if building in labs().keys():
            return self.build_lab(building)
        return self.build(building)

    def build(self, building):
        idle_workers_on_screen_count = self.count_idle_workers_on_screen()
        if building == units.Terran.Refinery \
                and not self.obs.free_vespene_geyser_on_screen():
            self.player_state.building_state.build_order_pos += 1
            self.remaining_executions -= 1
            self.reset_stage()
            return True

        if not self.building_affordable(building):
            return True

        if not self.worker_chosen or not self.obs.unit_type_selected(
                units.Terran.SCV):
            if idle_workers_on_screen_count < 1:
                self.select_units(units.Terran.SCV, 1)
                self.queue.append(FUNCTIONS.Stop_quick('now'))
                return False
            self.select_idle_worker_on_screen()
            self.worker_chosen = True
            return False

        action = building_action(building)
        building_possible = action.id in self.obs.obs.available_actions

        requirements = buildings_requirements().get(building, [])
        passed = all([
            self.obs.count_units_on_screen(req) > 0 for req
            in requirements
        ])

        if not passed:
            if all([
                self.obs.count_units_on_screen(req, False) > 0 for req
                in requirements
            ]):
                print('Waiting for requirements for building {0}'
                      .format(building))
                self.reset_stage()
                return True

            print('Requirements missing for building {0}'.format(building))
            self.player_state.building_state.build_order_pos += 1
            self.reset_stage()
            return True

        if not building_possible:
            raise EnvironmentError('Building {0} not possible'
                                   .format(building))

        self.player_state.building_state.currently_building = building
        location_for_building = self.location_for_building(building)
        self.count_of_building_during_order = self.obs.count_units_on_screen(
            building, False)
        self.steps_since_ordered_building = 0
        self.idle_workers_on_order = idle_workers_on_screen_count
        self.queue.append(action('now', location_for_building))
        return False

    def build_lab(self, lab):
        if not self.building_affordable(lab):
            return True

        parent_building = labs()[lab]
        building_count, lab_count = self.building_and_labs_count(
            parent_building)

        if lab_count >= building_count:
            return self.build(parent_building)

        if not self.lab_buildings_chosen:
            self.select_units(parent_building)
            self.lab_buildings_chosen = True
            return False

        if not self.queue_cleared_for_lab:
            # TODO handle the building queue
            self.queue_cleared_for_lab = True
            return False

        action = building_action(lab)
        lab_possible = action.id in self.obs.obs.available_actions
        if not lab_possible:
            raise EnvironmentError('Lab {0} not possible'.format(lab))

        self.queue.append(building_action('now'))
        self.reset_stage()
        return True

    def building_affordable(self, building):
        minerals = self.obs.obs.player.minerals
        vespene = self.obs.obs.player.vespene

        return building_cost(building) <= minerals \
            and building_cost_vespene(building) <= vespene

    def building_pass_requirements(self, building):
        requirements = buildings_requirements().get(building, None)
        if not requirements:
            return True
        return all([
            self.obs.count_units_on_screen(req) > 0 for req
            in requirements
        ])

    def building_and_labs_count(self, target_building):
        building_count = self.obs.count_units_on_screen(target_building)
        labs_count = sum([
            self.obs.count_units_on_screen(lab, False) for lab, building
            in labs().items()
            if building == target_building
        ])
        return building_count, labs_count

    def location_for_building(self, building_type):
        if building_type == units.Terran.Refinery:
            geysers = self.geysers_on_screen()
            if not geysers:
                raise NotImplementedError('No place for refinery')
            y, x = random.choice(geysers)
            return self.parameters.screen_point(x, y)

        minerals = self.minerals_on_screen()
        random_x = random.randint(5, 80)
        random_y = random.randint(5, 80)
        loc = self.parameters.screen_point(random_x, random_y)
        minerals_avg_loc = self.parameters.screen_point(0, 0)

        if minerals:
            sum_x = sum(map(lambda unit: unit.x, minerals))
            sum_y = sum(map(lambda unit: unit.y, minerals))
            minerals_avg_loc_x = sum_x / len(minerals)
            minerals_avg_loc_y = sum_y / len(minerals)
            minerals_avg_loc = self.parameters.screen_point(minerals_avg_loc_x,
                                                            minerals_avg_loc_y)

        loop_count = 0
        while self.location_wrong(loc, minerals_avg_loc):
            random_x = random.randint(10, 75)
            random_y = random.randint(10, 75)
            loc = self.parameters.screen_point(random_x, random_y)
            loop_count += 1
            if loop_count > 100000:
                break
        return loc

    # TODO take building type into consideration
    def location_wrong(self, loc, minerals_center):
        points = [
            Point(unit.x, unit.y) for unit
            in self.obs.obs.feature_units
        ]

        return any([
            loc.dist(point) < 10 for point
            in points
        ]) or not minerals_center.dist(loc) > 22

    def reset_stage(self):
        self.steps_since_ordered_building = None
        self.count_of_building_during_order = None
        self.idle_workers_on_order = None
        self.worker_chosen = False
        self.worker_moved = False
        self.player_state.building_state.currently_building = None
        self.lab_buildings_chosen = False
        self.queue_cleared_for_lab = False
        self.failed_attempts = 0

    def select_idle_worker_on_screen(self):
        worker = random.choice(self.idle_workers_on_screen())
        worker_loc = self.parameters.screen_point(worker.x, worker.y)
        self.queue.append(FUNCTIONS.select_point('select', worker_loc))

    def geysers_on_screen(self):
        geysers_types = [
            units.Neutral.VespeneGeyser,
            units.Neutral.RichVespeneGeyser
        ]

        return [
            unit for unit
            in self.obs.obs.feature_units
            if unit.unit_type in geysers_types
        ]

    def minerals_on_screen(self):
        minerals_types = [
            units.Neutral.MineralField,
            units.Neutral.MineralField750,
            units.Neutral.RichMineralField,
            units.Neutral.RichMineralField750
        ]

        return [
            unit for unit
            in self.obs.obs.feature_units
            if unit.unit_type in minerals_types
        ]

    def idle_workers_on_screen(self):
        return [
            unit for unit
            in self.obs.obs.feature_units
            if unit_is_idle_worker(unit)
        ]

    def count_idle_workers_on_screen(self):
        return len(self.idle_workers_on_screen())

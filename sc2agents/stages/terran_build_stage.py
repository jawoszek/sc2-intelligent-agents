"""A random agent for starcraft."""
import random
from pysc2.lib import actions, units
from pysc2.lib.point import Point
from sc2agents.stages.stage import Stage
from sc2agents.data.terran_state import TerranState
from sc2agents.data.terran_parameters import TerranParameters


FUNCTIONS = actions.FUNCTIONS


# TODO take building type into consideration
def location_wrong(obs, loc, minerals_center):
    points = [Point(unit.x, unit.y) for unit in obs.observation.feature_units]
    return any([loc.dist(point) < 10 for point in points]) or not minerals_center.dist(loc) > 22


# TODO proper logging
class TerranBuildStage(Stage):

    def __init__(self, state: TerranState, parameters: TerranParameters, stage_provider):
        super().__init__(3, state, parameters, stage_provider)
        self.steps_since_ordered_building = None
        self.count_of_building_during_order = None
        self.idle_workers_on_order = None
        self.worker_chosen = False
        self.worker_moved = False
        self.lab_buildings_chosen = False
        self.queue_cleared_for_lab = False
        self.failed_attempts = 0

    def process(self, obs):
        if not self.state.centered_at_cc():
            self.move_screen_to_cc()
            return

        if self.state.currently_building:
            # TODO enable after new pysc2 release
            # if not self.worker_moved and self.idle_workers_on_order <= self.count_idle_workers_on_screen(obs):
            #     print('Worker not started building')
            #     self.remaining_actions -= 1
            #     self.reset_stage()
            #     return
            # self.worker_moved = True
            if self.steps_since_ordered_building is not None:
                if self.count_units_on_screen(obs, self.state.currently_building, False) \
                        > self.count_of_building_during_order:
                    print('Built successfully')
                    self.state.build_order_pos += 1
                    self.state.add_building(self.state.currently_building)
                    self.reset_stage()
                    self.remaining_actions -= 1
                    return

                if self.steps_since_ordered_building > 20:
                    print('Abandoned due to timeout')
                    self.reset_stage()
                    self.remaining_actions -= 1
                    return

                self.steps_since_ordered_building += 1
                return
            self.reset_stage()
            self.remaining_actions -= 1
            return

        if self.next_build_order_reached(obs):
            should_pass_action = self.order_building(obs, self.parameters.build_order_building(self.state))
            if should_pass_action:
                self.remaining_actions -= 1
            return

        self.remaining_actions -= 1
        return

    def next_build_order_reached(self, obs):
        return self.parameters.build_order_reached(obs, self.state)

    def previous_building_built(self, obs):
        if self.state.build_order_pos < 1:
            return True

        previous_building = self.parameters.build_order_building(self.state, self.state.build_order_pos - 1)
        return self.count_units_on_screen(obs, previous_building) > 0

    def order_building(self, obs, building):
        if building in self.labs().keys():
            return self.build_lab(obs, building)
        return self.build(obs, building)

    def build(self, obs, building):
        # print("ordered building {0}".format(building))
        idle_workers_on_screen_count = self.count_idle_workers_on_screen(obs)
        if building == units.Terran.Refinery and not self.free_vespene_geyser_on_screen(obs):
            self.state.build_order_pos += 1
            self.remaining_actions -= 1
            self.reset_stage()
            return True

        if not self.building_affordable(obs, building):
            return True

        if not self.worker_chosen or not self.unit_type_selected(obs, units.Terran.SCV):
            if idle_workers_on_screen_count < 1:
                self.select_units(obs, units.Terran.SCV, 1)
                self.queue.append(FUNCTIONS.Stop_quick('now'))
                return False
            self.select_idle_worker_on_screen(obs)
            self.worker_chosen = True
            return False

        building_action = self.building_action(building)
        building_possible = building_action.id in obs.observation.available_actions

        requirements = self.buildings_requirements().get(building, None)
        passed = all([self.count_units_on_screen(obs, req) > 0 for req in requirements])

        if not passed:
            if all([self.count_units_on_screen(obs, req, False) > 0 for req in requirements]):
                print('Waiting for requirements for building {0}'.format(building))
                self.reset_stage()
                return True

            print('Requirements missing for building {0}'.format(building))
            self.state.build_order_pos += 1
            self.reset_stage()
            return True

        if not building_possible:
            raise EnvironmentError('Building {0} not possible'.format(building))

        self.state.currently_building = building
        location_for_building = self.location_for_building(obs, building)
        self.count_of_building_during_order = self.count_units_on_screen(obs, building, False)
        self.steps_since_ordered_building = 0
        self.idle_workers_on_order = idle_workers_on_screen_count
        self.queue.append(building_action('now', location_for_building))
        return False

    def build_lab(self, obs, lab):
        if not self.building_affordable(obs, lab):
            return True

        parent_building = self.labs()[lab]
        building_count, lab_count = self.building_and_labs_count(obs, parent_building)

        if lab_count >= building_count:
            return self.build(obs, parent_building)

        if not self.lab_buildings_chosen:
            self.select_units(obs, parent_building)
            self.lab_buildings_chosen = True
            return False

        if not self.queue_cleared_for_lab:
            # TODO handle the building queue
            self.queue_cleared_for_lab = True
            return False

        building_action = self.building_action(lab)
        lab_possible = building_action.id in obs.observation.available_actions
        if not lab_possible:
            raise EnvironmentError('Lab {0} not possible'.format(lab))

        self.queue.append(building_action('now'))
        self.reset_stage()
        return True

    def building_affordable(self, obs, building):
        return self.building_cost(building) <= obs.observation.player.minerals \
               and self.building_cost_vespene(building) <= obs.observation.player.vespene

    def building_pass_requirements(self, obs, building):
        requirements = self.buildings_requirements().get(building, None)
        if not requirements:
            return True
        return all([self.count_units_on_screen(obs, req) > 0 for req in requirements])

    @staticmethod
    def building_action(building):
        return {
            units.Terran.Refinery: FUNCTIONS.Build_Refinery_screen,
            units.Terran.SupplyDepot: FUNCTIONS.Build_SupplyDepot_screen,
            units.Terran.Barracks: FUNCTIONS.Build_Barracks_screen,
            units.Terran.CommandCenter: None,
            units.Terran.BarracksReactor: FUNCTIONS.Build_Reactor_quick,
            units.Terran.BarracksTechLab: FUNCTIONS.Build_TechLab_quick
        }[building]

    @staticmethod
    def buildings_requirements():
        return {
            units.Terran.Barracks: [units.Terran.SupplyDepot]
        }

    @staticmethod
    def building_cost(building):
        return {
            units.Terran.Refinery: 75,
            units.Terran.SupplyDepot: 100,
            units.Terran.Barracks: 150,
            units.Terran.CommandCenter: 400,
            units.Terran.BarracksReactor: 50,
            units.Terran.BarracksTechLab: 50
        }.get(building, 0)

    @staticmethod
    def building_cost_vespene(building):
        return {
            units.Terran.BarracksReactor: 50,
            units.Terran.BarracksTechLab: 25
        }.get(building, 0)

    @staticmethod
    def labs():
        return {
            units.Terran.BarracksReactor: units.Terran.Barracks,
            units.Terran.BarracksTechLab: units.Terran.Barracks
        }

    def building_and_labs_count(self, obs, target_building):
        building_count = self.count_units_on_screen(obs, target_building)
        labs_count = sum([
            self.count_units_on_screen(obs, lab, False)
            for lab, building in self.labs().items()
            if building == target_building
        ])
        return building_count, labs_count

    def location_for_building(self, obs, building_type):
        minerals_types = [
            units.Neutral.MineralField,
            units.Neutral.MineralField750,
            units.Neutral.RichMineralField,
            units.Neutral.RichMineralField750
        ]
        geysers_types = [
            units.Neutral.VespeneGeyser,
            units.Neutral.RichVespeneGeyser
        ]

        if building_type == units.Terran.Refinery:
            geysers = [unit for unit in obs.observation.feature_units if unit.unit_type in geysers_types]
            if not geysers:
                raise NotImplementedError('No place for refinery')
            chosen_geyser = random.choice(geysers)
            return self.parameters.screen_point(chosen_geyser.x, chosen_geyser.y)

        minerals = [unit for unit in obs.observation.feature_units if unit.unit_type in minerals_types]
        random_x = random.randint(5, 80)
        random_y = random.randint(5, 80)
        loc = self.parameters.screen_point(random_x, random_y)
        minerals_avg_loc = self.parameters.screen_point(0, 0)

        if minerals:
            sum_x = sum(map(lambda unit: unit.x, minerals))
            sum_y = sum(map(lambda unit: unit.y, minerals))
            minerals_avg_loc_x = sum_x / len(minerals)
            minerals_avg_loc_y = sum_y / len(minerals)
            minerals_avg_loc = self.parameters.screen_point(minerals_avg_loc_x, minerals_avg_loc_y)

        loop_count = 0
        while location_wrong(obs, loc, building_type, minerals_avg_loc):
            random_x = random.randint(10, 75)
            random_y = random.randint(10, 75)
            loc = self.parameters.screen_point(random_x, random_y)
            loop_count += 1
            if loop_count > 100000:
                return loc
        return loc

    def reset_stage(self):
        self.steps_since_ordered_building = None
        self.count_of_building_during_order = None
        self.idle_workers_on_order = None
        self.worker_chosen = False
        self.worker_moved = False
        self.state.currently_building = None
        self.lab_buildings_chosen = False
        self.queue_cleared_for_lab = False
        self.failed_attempts = 0

    def select_idle_worker_on_screen(self, obs):
        worker = random.choice(self.get_idle_workers_on_screen(obs))
        worker_loc = self.parameters.screen_point(worker.x, worker.y)
        self.queue.append(FUNCTIONS.select_point('select', worker_loc))

    @staticmethod
    def get_idle_workers_on_screen(obs):
        return [unit for unit in obs.observation.feature_units if TerranBuildStage.unit_is_idle_worker(unit)]

    @staticmethod
    def count_idle_workers_on_screen(obs):
        return len(TerranBuildStage.get_idle_workers_on_screen(obs))

    @staticmethod
    def unit_is_idle_worker(unit):
        return unit.unit_type == units.Terran.SCV  # and unit.order_length == 0 TODO add after new pysc2 release

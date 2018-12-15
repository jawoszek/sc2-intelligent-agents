"""A random agent for starcraft."""
import random

from pysc2.lib import actions

from sc2agents.data.control_state import MAIN_GROUP
from sc2agents.data.observations import Observations
from sc2agents.data.parameters import Parameters
from sc2agents.data.player_state import PlayerState

FUNCTIONS = actions.FUNCTIONS


def point_in_range(source, target, dist_range):
    return source.dist(target) <= dist_range


def point_in_range_for_any(target, points, dist_range):
    return any([
        point for point
        in points
        if point_in_range(target, point, dist_range)
    ])


class Stage:

    def __init__(self,
                 remaining_executions: int,
                 parameters: Parameters,
                 player_state: PlayerState):

        self.remaining_executions = remaining_executions
        self.parameters = parameters
        self.player_state = player_state
        self.queue: list = []
        self.obs: Observations = None

    def prepare(self, _):
        self.queue.append(FUNCTIONS.select_control_group('recall', MAIN_GROUP))

    def process(self, obs: Observations):
        self.obs = obs

    def has_next_action(self):
        return self.queue

    def next_action(self):
        return self.queue.pop()

    def ended(self):
        return self.remaining_executions < 1

    def move_screen(self, loc):
        map_state = self.player_state.map_state
        map_state.current_loc = loc
        map_state.centered_at_base = loc == map_state.current_main_base_loc
        self.queue.append(FUNCTIONS.move_camera(loc))

    def move_screen_to_cc(self):
        self.move_screen(self.player_state.map_state.current_main_base_loc)

    def select_units(self, unit_type, count: int = None):
        units_on_screen = self.obs.units_on_screen(unit_type)

        if not units_on_screen:
            raise EnvironmentError('No units to select found')

        if count is None:
            unit_to_select = random.choice(units_on_screen)
            unit = self.parameters.screen_point(unit_to_select.x,
                                                unit_to_select.y)
            self.queue.append(FUNCTIONS.select_point('select_all_type', unit))
        elif count >= 1:
            units_to_select = random.choices(units_on_screen, k=count)
            x, y = units_to_select[0].x, units_to_select[0].y
            first_unit_loc = self.parameters.screen_point(x, y)
            self.queue.append(FUNCTIONS.select_point('select', first_unit_loc))
            for unit in units_to_select[1:]:
                next_unit = self.parameters.screen_point(unit.x, unit.y)
                self.queue.append(FUNCTIONS.select_point('toggle', next_unit))

    def select_army(self):
        self.queue.append(FUNCTIONS.select_army("select"))

    def closest_expansion_loc(self, also_visible=False):
        return self.sorted_expansions(also_visible)[0]

    def furthest_expansion_loc(self, also_visible=False):
        return self.sorted_expansions(also_visible, True)[0]

    def sorted_expansions(self, also_visible=False, desc=False):
        expansions = self.all_expansion_locations(also_visible)
        return sorted(expansions,
                      key=self.distance_from_base_to_loc,
                      reverse=desc)

    def all_expansion_locations(self, also_visible=False):
        y, x = self.obs.neutral_on_minimap()
        expansions = self.locations_to_points(x, y, screen=False)
        if also_visible:
            return expansions
        visible = self.obs.visible_minimap()
        return [
            expansion for expansion
            in expansions
            if expansion not in visible
        ]

    def visible_minimap(self):
        v_y, v_x = self.obs.visible_minimap()
        return self.locations_to_points(v_x, v_y, screen=False)

    def locations_to_points(self, x, y, screen=True):
        screen_transform = self.parameters.screen_point
        minimap_transform = self.parameters.minimap_point
        transform = screen_transform if screen else minimap_transform
        return list(map(lambda xy: transform(xy[0], xy[1]), zip(x, y)))

    def distance_from_base_to_loc(self, loc):
        return self.player_state.map_state.current_main_base_loc.dist(loc)

    def positions_of_enemy_on_minimap(self, only_visible=False,
                                      distance_from_visible=None):
        y, x = self.obs.enemy_on_minimap()
        enemies = self.locations_to_points(x, y, screen=False)
        if not only_visible:
            return enemies
        visible = self.visible_minimap()

        if distance_from_visible is not None:
            return [
                enemy for enemy
                in enemies
                if point_in_range_for_any(enemy,
                                          visible,
                                          distance_from_visible)]

        return [
            enemy for enemy
            in enemies
            if enemy in visible
        ]

    def potential_enemy_base_locations(self):
        map_state = self.player_state.map_state
        x = map_state.current_main_base_loc.x
        y = map_state.current_main_base_loc.y
        minimap_size = map_state.minimap_size

        return [
            self.parameters.minimap_point(minimap_size - x, minimap_size - y),
            self.parameters.minimap_point(minimap_size - x, y),
            self.parameters.minimap_point(x, minimap_size - y)
        ]

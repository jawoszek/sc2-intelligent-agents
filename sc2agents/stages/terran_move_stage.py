"""A random agent for starcraft."""
import random
from pysc2.lib import actions, features
from sc2agents.data.terran_state import TerranState
from sc2agents.data.terran_parameters import TerranParameters
from sc2agents.stages.stage import Stage


FUNCTIONS = actions.FUNCTIONS


class TerranMoveStage(Stage):

    def __init__(self, state: TerranState, parameters: TerranParameters, stage_provider):
        super().__init__(1, state, parameters, stage_provider)
        self.army_selected = False

    def process(self, obs):
        enemies_location_minimap_visible = self.get_positions_of_enemy_on_minimap(obs, only_visible=True,
                                                                                  distance_from_visible=8)

        if enemies_location_minimap_visible and self.can_select_army(obs):
            self.select_army()
            if not self.army_selected:
                self.select_army()
                self.army_selected = True
                return

            attack_target = self.closest_free_point(obs, enemies_location_minimap_visible[0])
            self.queue.append(FUNCTIONS.Attack_minimap('now', attack_target))
            self.remaining_actions -= 1
            return

        enemies_location_minimap = self.get_positions_of_enemy_on_minimap(obs)

        if enemies_location_minimap and self.can_select_army(obs) and self.should_attack(obs):
            self.select_army()
            if not self.army_selected:
                self.select_army()
                self.army_selected = True
                return

            target = enemies_location_minimap[0]
            attack_target = self.closest_free_point(obs, target)
            self.queue.append(FUNCTIONS.Attack_minimap('now', attack_target))
            self.remaining_actions -= 1
            return

        self.remaining_actions -= 1
        return

    def closest_free_point(self, obs, target):
        minimap = obs.observation.feature_minimap.player_id
        queue = [target]
        already = {target}
        while queue:
            current = queue.pop()
            if minimap[current.y][current.x] == features.PlayerRelative.NONE:
                return current
            nearby_points = self.nearby_points(current)
            for point in nearby_points:
                if point not in already:
                    queue.append(point)
                    already.add(point)
        print('No free close-by target')
        return target

    def nearby_points(self, point):
        points = [
            self.parameters.minimap_point(point.x - 1, point.y),
            self.parameters.minimap_point(point.x, point.y - 1),
            self.parameters.minimap_point(point.x + 1, point.y),
            self.parameters.minimap_point(point.x, point.y + 1)
        ]
        random.shuffle(points)
        return points

    @staticmethod
    def should_attack(obs):
        return obs.observation.player.food_army > 30

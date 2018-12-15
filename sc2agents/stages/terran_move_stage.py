"""A random agent for starcraft."""
import random

from pysc2.lib import actions, features

from sc2agents.data.parameters import Parameters
from sc2agents.data.player_state import PlayerState
from sc2agents.stages.stage import Stage

FUNCTIONS = actions.FUNCTIONS


class TerranMoveStage(Stage):

    def __init__(self,
                 parameters: Parameters,
                 player_state: PlayerState):

        super().__init__(1, parameters, player_state)
        self.army_selected = False

    def process(self, obs):
        super(TerranMoveStage, self).process(obs)
        enemies_visible_on_minimap = self.positions_of_enemy_on_minimap(
            only_visible=True, distance_from_visible=8)

        if enemies_visible_on_minimap and self.obs.can_select_army():
            self.select_army()
            if not self.army_selected:
                self.select_army()
                self.army_selected = True
                return

            attack_target = self.closest_free_point(
                enemies_visible_on_minimap[0])
            self.queue.append(FUNCTIONS.Attack_minimap('now', attack_target))
            self.remaining_executions -= 1
            return

        enemies_on_minimap = self.positions_of_enemy_on_minimap()

        if enemies_on_minimap and self.obs.can_select_army() \
                and self.should_attack():
            self.select_army()
            if not self.army_selected:
                self.select_army()
                self.army_selected = True
                return

            target = enemies_on_minimap[0]
            attack_target = self.closest_free_point(target)
            self.queue.append(FUNCTIONS.Attack_minimap('now', attack_target))

        self.remaining_executions -= 1
        return

    def closest_free_point(self, target):
        minimap = self.obs.obs.feature_minimap.player_id
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
        # TODO proper logging
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

    def should_attack(self):
        return self.obs.player.food_army > 30

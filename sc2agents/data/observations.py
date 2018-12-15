"""A random agent for starcraft."""
from pysc2.lib import actions, features, units

FUNCTIONS = actions.FUNCTIONS


def count_selected_unit_type(obs, unit_type):
    if obs.single_select.any() and obs.single_select[0].unit_type == unit_type:
        return 1
    if obs.multi_select.any():
        return len([
            unit for unit
            in obs.multi_select
            if unit.unit_type == unit_type
        ])
    return 0


def units_on_screen(obs, unit_type, only_ready):
    def is_required_unit_type(unit):
        return unit_type is None or unit.unit_type == unit_type

    def is_ready_if_needed(unit):
        return not only_ready or unit.build_progress in [0, 100]

    return [
        unit for unit
        in obs.feature_units
        if is_required_unit_type(unit) and is_ready_if_needed(unit)
    ]


def relative_on_minimap(obs, relative_id):
    players_units = obs.feature_minimap.player_relative
    return (players_units == relative_id).nonzero()


class Observations:

    def __init__(self, obs):
        self.obs = obs.observation
        self.player = obs.observation.player
        self.timestep = obs

    def unit_type_selected(self, unit_type, required_count=None):
        unit_count = count_selected_unit_type(self.obs, unit_type)

        if required_count is None:
            return unit_count > 0

        return unit_count == required_count

    def units_on_screen(self, unit_type=None, only_ready=True):
        return units_on_screen(self.obs, unit_type, only_ready)

    def count_units_on_screen(self, unit_type=None, only_ready=True):
        return len(units_on_screen(self.obs, unit_type, only_ready))

    def can_select_army(self):
        return FUNCTIONS.select_army.id in self.obs.available_actions

    def enemy_on_minimap(self):
        enemy_id = features.PlayerRelative.ENEMY
        return relative_on_minimap(self.obs, enemy_id)

    def neutral_on_minimap(self):
        neutral_id = features.PlayerRelative.NEUTRAL
        return relative_on_minimap(self.obs, neutral_id)

    def visible_minimap(self):
        visibility = self.obs.feature_minimap.visibility_map
        visible_id = features.Visibility.VISIBLE
        return (visibility == visible_id).nonzero()

    def free_vespene_geyser_on_screen(self):
        geysers = {
            units.Neutral.VespeneGeyser,
            units.Neutral.RichVespeneGeyser
        }
        refineries = {
            units.Terran.Refinery,
            units.Zerg.Extractor,
            units.Protoss.Assimilator
        }
        geysers_count = sum([
            1 for unit
            in self.obs.feature_units
            if unit.unit_type in geysers
        ])

        # TODO fix geyser coming into screen from another expansion
        geysers_count = min(geysers_count, 2)

        refineries_count = sum([
            1 for unit
            in self.obs.feature_units
            if unit.unit_type in refineries
        ])
        return geysers_count > refineries_count

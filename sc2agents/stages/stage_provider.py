"""A random agent for starcraft."""

from sc2agents.stages.terran_refresh_state_stage import TerranRefreshStateStage
from sc2agents.stages.terran_build_stage import TerranBuildStage
from sc2agents.stages.terran_move_stage import TerranMoveStage
from sc2agents.stages.terran_recruit_stage import TerranRecruitStage
from sc2agents.stages.terran_scout_stage import TerranScoutStage

STAGE_SUCCESSOR = {
    type(None): TerranRefreshStateStage,
    TerranRefreshStateStage: TerranRecruitStage,
    TerranRecruitStage: TerranMoveStage,
    TerranMoveStage: TerranScoutStage,
    TerranScoutStage: TerranBuildStage,
    TerranBuildStage: TerranRecruitStage
}


class StageProvider:  # pylint: disable=too-few-public-methods

    @staticmethod
    def provide_next_stage(stage):
        return STAGE_SUCCESSOR[type(stage)]

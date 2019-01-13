"""A terran agent."""
from enum import Enum

import sc2agents.data.terran as terran


class Race(Enum):
    TERRAN = terran
    ZERG = None
    PROTOSS = None

    def constants(self):
        return self.value.constants

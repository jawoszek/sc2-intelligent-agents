"""A random agent for starcraft."""
from pysc2.lib import actions, units

FUNCTIONS = actions.FUNCTIONS

UNIT_TO_BUILDING = {
    units.Terran.SCV: units.Terran.CommandCenter,
    units.Terran.Marine: units.Terran.Barracks
}

UNIT_TO_COST = {
    units.Terran.SCV: 50,
    units.Terran.Marine: 50
}

UNIT_TO_ACTION = {
    units.Terran.SCV: FUNCTIONS.Train_SCV_quick,
    units.Terran.Marine: FUNCTIONS.Train_Marine_quick
}

BUILDING_TO_ACTION = {
    units.Terran.Refinery: FUNCTIONS.Build_Refinery_screen,
    units.Terran.SupplyDepot: FUNCTIONS.Build_SupplyDepot_screen,
    units.Terran.Barracks: FUNCTIONS.Build_Barracks_screen,
    units.Terran.CommandCenter: None,
    units.Terran.BarracksReactor: FUNCTIONS.Build_Reactor_quick,
    units.Terran.BarracksTechLab: FUNCTIONS.Build_TechLab_quick
}

BUILDING_TO_COST = {
    units.Terran.Refinery: 75,
    units.Terran.SupplyDepot: 100,
    units.Terran.Barracks: 150,
    units.Terran.CommandCenter: 400,
    units.Terran.BarracksReactor: 50,
    units.Terran.BarracksTechLab: 50
}

BUILDING_TO_COST_VESPENE = {
    units.Terran.BarracksReactor: 50,
    units.Terran.BarracksTechLab: 25
}

BUILDING_TO_REQUIREMENTS = {
    units.Terran.Barracks: [units.Terran.SupplyDepot]
}

LAB_TO_BUILDING = {
    units.Terran.BarracksReactor: units.Terran.Barracks,
    units.Terran.BarracksTechLab: units.Terran.Barracks
}

INITIAL_UNITS = {
    units.Terran.SCV: 12
}

INITIAL_BUILDINGS = {
    units.Terran.CommandCenter: 1
}

RECRUIT_ORDER_DEFAULT = [
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.Marine,
    units.Terran.SCV,
    units.Terran.Marine,
    units.Terran.SCV,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine
]

BUILD_ORDER_DEFAULT = [
    (12, units.Terran.SupplyDepot),
    (14, units.Terran.Barracks),
    (16, units.Terran.SupplyDepot),
    (17, units.Terran.Refinery),
    (18, units.Terran.Barracks),
    (19, units.Terran.SupplyDepot),
    (22, units.Terran.Barracks),
    (23, units.Terran.Refinery),
    (24, units.Terran.SupplyDepot),
    (28, units.Terran.Barracks),
    (34, units.Terran.SupplyDepot),
    (40, units.Terran.SupplyDepot),
    (48, units.Terran.SupplyDepot),
    (56, units.Terran.SupplyDepot),
    (64, units.Terran.SupplyDepot)
]

UNITS_TO_CHOOSE = [
    units.Terran.SCV,
    units.Terran.Marine
]

BUILDINGS_TO_CHOOSE = [
    units.Terran.SupplyDepot,
    units.Terran.Barracks,
    units.Terran.Refinery
]

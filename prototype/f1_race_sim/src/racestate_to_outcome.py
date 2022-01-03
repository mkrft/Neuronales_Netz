#=====Module Imports==================================
from src.config import (
    RACE_DISTANCE,
    REFERANCE_LAP_TIME,
)

from src.const import (
    SOFT,
    MEDIUM,
    HARD
)

from src.const import GRID_CACHE
from src.laptime import compute_lap_times
from src.display import test_print
from src.overtake import overtaking
from src.order_grid import order_grid


def get_output(input_vector):
    """
    Take a game state and a driver and return the race data from there
    """
    
    current_lap = input_vector[0]

    while current_lap < RACE_DISTANCE:

        for car in GRID_CACHE:
            pass


def reconstruct_state(environment_list):


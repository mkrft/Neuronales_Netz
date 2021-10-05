"""
    Module to contain the main race loop
    to simulate a full "lap" around the virtual circut
"""

#=====Imports=========================================

#=====Module Imports==================================
from src.config import (
    RACE_DISTANCE,
    REFERANCE_LAP_TIME
)

from src.const import GRID_CACHE
from src.laptime import compute_lap_times
from src.display import test_print

#=====Libraries=======================================


#=====Functions=======================================
def race_loop():
    
    # Init the current lap with the starting lap of 0
    current_lap = 0

    # "Race" until the RACE_DISTANCE is reached
    while current_lap < RACE_DISTANCE:

        for car in GRID_CACHE:

            # TODO Compute the needed lap time
            needed_lap_time = compute_lap_times(car)

            car.race_time += needed_lap_time

            # TODO Add tyre degredation

        # TODO Check for overtakes
        # TODO Define rules for overtaking like a probability function concerning the intervals after the "last" lap
        # TODO Compute the invervals and store them somewhere to get the from there again... maybe as attribute of a car?

        # TODO Add possibility of a pitstop in this lap
        # TODO this means adding pitstop delta time to race_time and changing tyre to new ones that are fresh

        # End active lap
        current_lap += 1

        # Display the current standigs
        test_print(current_lap)

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

            # Compute the needed lap time
            needed_lap_time = compute_lap_times(car)

            car.race_time += needed_lap_time

            

            # TODO Check for overtakes
            # TODO Define rules for overtaking like a probability function concerning the intervals after the "last" lap
            
            # TODO Compute the invervals!

            # Determine if the car has increased tyre degradation or not
            if car.delta_to_car_infront <= 1.0:
                close_car_infront = True
            else:
                close_car_infront = False
            
            # Let the tyre degrade according to the interval to car infront
            if close_car_infront:
                car.tyre.degrade(car_infront=True)
            else:
                car.tyre.degrade()

            # TODO Add possibility of a pitstop in this lap
            # TODO this means adding pitstop delta time to race_time and changing tyre to new ones that are fresh


        # End active lap
        current_lap += 1

        # Display the current standigs
        test_print(current_lap)

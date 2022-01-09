"""
    Module to contain the main race loop
    to simulate a full "lap" around the virtual circut
"""

#=====Module Imports==================================
from src.config import (
    RACE_DISTANCE,
    REFERANCE_LAP_TIME,
    CURRENT_RACE_LAP
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


#=====Functions=======================================
def race_loop(print_opt=True):
    
    # Init the current lap with the starting lap of 0
    current_lap = 0
    racedata = []

    # "Race" until the RACE_DISTANCE is reached
    while CURRENT_RACE_LAP[0] < RACE_DISTANCE:

        for car in GRID_CACHE:

            # Compute the needed lap time
            needed_lap_time = compute_lap_times(car)
            car.race_time = round(car.race_time + needed_lap_time, 2)
            car.last_lap = needed_lap_time

            # Determine if the car has increased tyre degradation or not
            # TODO add function to correlate delta with the penalty
            if car.delta_to_car_infront == "-":
                close_car_infront = False
            elif car.delta_to_car_infront <= 1.0 and car.position != 1:
                close_car_infront = True
            else:
                close_car_infront = False
            
            # Let the tyre degrade according to the interval to car infront
            if close_car_infront:
                car.tyre.degrade(car_infront=True)
            else:
                car.tyre.degrade()

            # TODO How to decide wether to pit and on which tyre
            # TODO How to give this option to the AI?
            # TODO Only test implementation
            if CURRENT_RACE_LAP[0] == 25: 
                car.pitstop(MEDIUM)


        # Sort the whole grid and set the accoridng intervals
        grid_sorted = order_grid()
        

        # Check for potential overtakes and let them happen
        # TODO Overtakes can still happen just by having a quicker lap...
        overtaking(grid_sorted)

        grid_sorted = order_grid()
        racedata.append(grid_sorted)

        # End active lap
        CURRENT_RACE_LAP[0] += 1

        # TODO Check if last lap and everyone has fullfilled the rule of changeing tyres at least once to different compound

        # Display the current standings
        if print_opt:
            test_print(current_lap, grid_sorted)

    return racedata 

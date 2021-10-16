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

from src.const import (
    SOFT,
    MEDIUM,
    HARD
)

from src.const import GRID_CACHE
from src.laptime import compute_lap_times
from src.display import test_print
from src.overtake import check_overtake

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
            car.race_time = round(car.race_time + needed_lap_time, 2)

            # Determine if the car has increased tyre degradation or not
            # TODO add function to corelate delta with the penalty
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
            if current_lap == 25: 
                car.pitstop(MEDIUM)


        # Order grid by race time at the end of the lap
        grid_sorted = sorted(GRID_CACHE, key=lambda car: car.race_time)

        # Alter the positions according to race time
        for index in range(0, len(grid_sorted)):

            # Set the new position of this lap
            grid_sorted[index].position = index + 1

            # Compute the according intervals
            # But skip the driver on pos one
            if index == 0:
                grid_sorted[index].delta_to_car_infront = "-"
                continue

            grid_sorted[index].delta_to_car_infront = round(grid_sorted[index].race_time - grid_sorted[index - 1].race_time, 2)

        # TODO Check for overtakes
        # TODO Define rules for overtaking like a probability function concerning the intervals after the "last" lap
        for index in range(0, len(grid_sorted)):
            
            if grid_sorted[index].delta_to_car_infront <= OVERTAKE_TRESHOLD:

                check_overtake(grid_sorted[index], grid_sorted[index - 1])

        # End active lap
        current_lap += 1

        # TODO Check if last lap and everyone has fullfilled the rule of changeing tyres at least once to different compound

        # Display the current standigs
        test_print(current_lap, grid_sorted)

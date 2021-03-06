"""
    Module to contain the main race loop
    to simulate a full "lap" around the virtual circut
"""

#=====Imports=========================================
import random

#=====Module Imports==================================
from src.config import (
    RACE_DISTANCE,
    REFERANCE_LAP_TIME,
)

from src.actions import Actions
from src.laptime import compute_lap_times
from src.display import display_standings
from src.overtake import check_overtake
from src.order_grid import order_grid
from src.customerrors import RaceError


#=====Functions=======================================
def race_loop(grid : list, print_opt : bool=True) -> None:
    """
    Function that shall represent our main loop, in which
    all computations are done per car for every single lap
    in order of the grid to have a coherent behaviour

    param - {list[cars]} - grid

    """
    
    # Init the current lap with the starting lap of 0
    current_lap = 0

    # "Race" until the RACE_DISTANCE is reached
    while current_lap < RACE_DISTANCE:

        # Reset this param every lap
        lap_time_car_infront = 0

        for position, car in enumerate(grid):

            # Compute lap time the car needs
            calc_lap_time = compute_lap_times(car)

            # Tyre life get increased by a lap
            car.tyre.tyre_life += 1


            # Now check if you make overtook a car by having a faster laptime, if so calc if your overtake is successful
            # If not make sure the calc_lap_time will be slower than the lap_time_car_infront so it wont be overtaken easily
            if calc_lap_time < lap_time_car_infront:
                if car.delta_to_car_infront <= abs(calc_lap_time - lap_time_car_infront):

                    # Check if the current car is able to make the overtake
                    # If so just leave the times as they were
                    if check_overtake(pace_diff=abs(calc_lap_time - lap_time_car_infront)-car.delta_to_car_infront):
                        print(f"{car.driver.short} overtook {grid[position - 1].driver.short}")

                    # If not "slow" the car down that was not able to overtake, so it stays behind
                    else:
                        calc_lap_time = lap_time_car_infront + round(random.uniform(0.2, 0.8), 3)


            # Apply the new lap time to the whole race time and update the reference lap for the next car
            car.race_time = round(car.race_time + calc_lap_time, 2)
            lap_time_car_infront = calc_lap_time
            

            # Let the tyre degrade according to the interval to car infront
            # try / except for the car on pos 1 that has the string "-" as delta, therefore no one in front and we can degrade without penalty
            try:
                if car.delta_to_car_infront <= 1:
                    car.tyre.degrade(car_infront=True)
                else:
                    car.tyre.degrade()
            except TypeError:
                car.tyre.degrade()

            # Static Pitstop for the whole field
            if current_lap == 25: 
                car.pitstop(Actions.MEDIUM)


        # Sort the whole grid and set the accoridng intervals
        grid = order_grid(grid)

        # End active lap
        current_lap += 1

        # Disqualify a car that hasnt used two distinctive tyre compounds
        if(current_lap == RACE_DISTANCE):
            for car in grid:
                if(car.distinctUsedTyreTypes() < 2):
                    car.position = "DSQ"



        # Display the current standings
        display_standings(current_lap, grid)

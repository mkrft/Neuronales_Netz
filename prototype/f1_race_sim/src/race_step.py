""" 
    Step function of the environment, corresponding to a single lap od the race
"""

#===== MODULE IMPORTS ================================
from src.config import (
    RACE_DISTANCE
)

from src.race_step_helpers import (
    take_action,
    give_lap_rewards,
    give_race_rewards
)
from src.laptime import compute_lap_times
from src.overtake import check_overtake
from src.order_grid import order_grid

#===== IMPORTS =======================================
import random
import copy

#====== FUNCTION =====================================
def step(grid, actions, lap, log):
    """
    Do all the cars' actions
    return the new state as the cars in the grid
    """

    initial_grid = copy.deepcopy(grid)

    # reset every lap
    lap_time_car_infront = 0

    for position, car in enumerate(grid):

        # Compute the needed lap time
        calc_lap_time = compute_lap_times(car)

        # Tyre life gets increased by one lap
        car.tyre.tyre_life += 1

        # Now check if you make overtook a car by having a faster laptime, if so calc if your overtake is successful
        if (calc_lap_time < lap_time_car_infront) and (car.delta_to_car_infront != "-"):
            if car.delta_to_car_infront <= abs(calc_lap_time - lap_time_car_infront):
               
                # Check if the current car is able to make the overtake
                # If not "slow" the car down that was not able to overtake, so it stays behind
                if not check_overtake(pace_diff=abs(calc_lap_time - lap_time_car_infront)-car.delta_to_car_infront):
                    calc_lap_time = lap_time_car_infront + round(random.uniform(0.2, 0.8), 3)

        # Apply the new lap time to the whole race time and update the reference lap for the next car
        car.race_time = round(car.race_time + calc_lap_time, 2)
        car.last_lap_time = calc_lap_time
        lap_time_car_infront = calc_lap_time
 
        # Let the tyre degrade according to the interval to car infront
        # try / except for the car on pos 1 that has the string "-" as delta, therefore no one in front and we can degrade without penalty
        try:
            if car.delta_to_car_infront <= 1:
                car.tyre.degrade(car_infront=True, delta_to_car_infront=car.delta_to_car_infront)
            else:
                car.tyre.degrade()
        except TypeError:
            car.tyre.degrade()

        # Have the car make its action defined in the actions dictionary
        take_action(car, actions)

    # Sort the gird per position
    grid_sorted = order_grid(grid)

    # Store logging data
    if log:
        for car in grid:
            car.store_logging_data(lap=lap)

    # Finish current lap
    lap += 1

    # Compute rewards
    rewards = give_lap_rewards(actions, initial_grid, grid)

    # If tha last lap is reached, check for Integrity of tyre rules
    # and apply rewards based on race result as whole
    if lap == RACE_DISTANCE:
        for car in grid:
             if(car.distinctUsedTyreTypes() < 2):                    
                 car.disqualify()
        rewards = give_race_rewards(actions, grid)

    # Finish step with the current grid, number of laps driven and the rewards for all cars
    return grid, lap, rewards

"""
    Module to handle the process of overtaking

"""

#=====Imports=========================================
import random

#=====Module Imports==================================
from src.config import (
    OVERTAKE_TRESHOLD
)


#=====Libraries=======================================


#=====Functions=======================================
def check_overtake(car, car_infront):
    """
    Function to determine the probability of an overtake
    and return an according bool if overtake is succesful or not

    param - {obj} - car - Instance if Class Car that is trying to overtake
    param - {obj} - car_infront - Instance of Class Car that is in front

    return - {bool} - overtake_done
    """

    # TODO Whole function could be a single line :D i think

    # Init
    overtake_done = False

    # Probability Function
    # TODO Add Function that takes delta, tyres, power, skill into consideration
    probability = 0.15

    # Check if car is able to overtake
    if round(random.uniform(0.0, 1.0), 2) <= probability:
        overtake_done = True 

    return overtake_done


def overtaking(grid_sorted):
    """
    Function for handling the overtake rules and
    to actually perform the overtakes

    param - {list} - gird_sorted - List of pointers to all car objects
    """

    # Check for every car expect the leader
    for index in range(1, len(grid_sorted)):

        # Check if car is in reach for a potential overtake
        if grid_sorted[index].delta_to_car_infront <= OVERTAKE_TRESHOLD:

            # Check the odds of the Overtake being succesfull
            if check_overtake(car=grid_sorted[index], car_infront=grid_sorted[index - 1]):

                # Switch the position and the race_times as "overtake"
                pos_cache = grid_sorted[index].position
                race_time_cache = grid_sorted[index].race_time

                grid_sorted[index].position = grid_sorted[index - 1].position
                grid_sorted[index].race_time = grid_sorted[index - 1].race_time

                grid_sorted[index - 1].position = pos_cache
                grid_sorted[index - 1].race_time = race_time_cache

                print(f"{grid_sorted[index].driver.short} overtook {grid_sorted[index - 1].driver.short}")
"""
    Module to hold the print functions for visualization
"""

#=====Imports=========================================

#=====Module Imports==================================
from src.const import GRID_CACHE

#=====Libraries=======================================


#=====Functions=======================================
def test_print(current_lap):
    """
    Give a full overview of the current standings
    """

    print(f"Current Lap: {current_lap}")
    print("| Driver | Pos |    Tyre   |    RaceTime    | Interval |")
    for car in GRID_CACHE:
        print(f"|  {car.driver.short}   |  {car.position}  |  {car.tyre.compound} {round(car.tyre.degredation * 100, 2)}%   |     {car.race_time}    |   {car.delta_to_car_infront}   |")
    print("\n")
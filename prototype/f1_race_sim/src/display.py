"""
    Module to hold the print functions for visualization
"""

#=====Imports=========================================

#=====Module Imports==================================
from src.const import GRID_CACHE

#=====Libraries=======================================
from prettytable import PrettyTable

#=====Functions=======================================
def test_print(current_lap):
    """
    Give a full overview of the current standings
    """

    # Build table output
    output = PrettyTable()
    output.field_names = ["POS", "DRIVER", "TYRE", "RACE TIME", "INTERVAL"]

    # Order grid by race time
    grid_sorted = sorted(GRID_CACHE, key=lambda car: car.race_time)

    for car in grid_sorted:
        output.add_row([car.position, car.driver.short, f"{car.tyre.compound} {round(car.tyre.degredation * 100, 2)}%", car.race_time, car.delta_to_car_infront])

    print(f"Current Race Lap:\t{current_lap}")
    print(output)
    print("\n")
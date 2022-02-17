"""
    Module to hold the print functions for visualization
"""


#=====Libraries=======================================
from prettytable import PrettyTable


#=====Functions=======================================
def test_print(current_lap, grid_sorted):
    """
    Give a full overview of the current standings
    """

    # Build table output
    output = PrettyTable()
    output.field_names = ["POS", "DRIVER", "  TYRE  ", "RACE TIME", " INTERVAL ", "STARTED ON"]

    for car in grid_sorted:
        output.add_row([car.position, car.driver.short, f"{car.tyre.compound} {round(car.tyre.degredation * 100, 2)}%", car.race_time, f"+ {car.delta_to_car_infront}", car.grid_position])

    print(f"Current Race Lap:\t{current_lap}")
    print(output)
    print("\n")
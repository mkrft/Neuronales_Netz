"""
    Module to hold the print functions for visualization
"""


#=====Libraries=======================================
from prettytable import PrettyTable
from colorama import Fore, Style


#=====Functions=======================================
def display_standings(current_lap, grid_sorted):
    """
    Give a full overview of the current standings
    """

    # Build table output
    output = PrettyTable()
    output.field_names = ["POS", "DRIVER", "  TYRE  ", "RACE TIME", " INTERVAL ", "STARTED ON"]

    #Defining the colortheme
    color = Fore.GREEN
    for car in grid_sorted:

        # Ensure that only the ai car is beeing colored
        if str(car.driver.short).__contains__("DKI"):
            position_field = car.position if car.position != "DSQ" else "DSQ"
            
            # Add a row to the table with all entries being colored individually            
            output.add_row([ color + f"{position_field}" + Style.RESET_ALL,
                            color + car.driver.short + Style.RESET_ALL,
                            color + f"{car.tyre.compound} {round(car.tyre.degredation * 100, 2)}%" + Style.RESET_ALL,
                            color + f"{round(car.race_time,2)}" + Style.RESET_ALL,
                            color + f"+ {car.delta_to_car_infront}" + Style.RESET_ALL,
                            color + f"{car.grid_position}" + Style.RESET_ALL])
            continue            
        
        output.add_row([car.position, car.driver.short, f"{car.tyre.compound} {round(car.tyre.degredation * 100, 2)}%", car.race_time, f"+ {car.delta_to_car_infront}", car.grid_position])

    print(f"Current Race Lap:\t{current_lap}")
    print(output)
    print("\n")

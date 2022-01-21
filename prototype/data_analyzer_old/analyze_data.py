"""
    This module shall serve as web crawler for every bit of
    data we can get concerning a formula 1 race.

    Therefore we use the Formula One API grom ergast.com
    https://documenter.getpostman.com/view/11586746/SztEa7bL
    http://ergast.com/mrd/

    author:     Alexander Müller
    date:       15.12.2021
    version.    0.0.1

    Written for educational purposes only.
"""

#=====Imports=========================================
import argparse

#=====Module Imports==================================
from src.visualize_data import plot_driver_lap_times
from src.get_race_data import (
    get_race_data,
    get_lap_data,
    output_race_data
)


#=====Functions=======================================
def parse_args():
    """
    Simple argument handler
    """

    # Create Handler
    arg_parser = argparse.ArgumentParser()

    # Define arguments
    arg_parser.add_argument("-y", type=int, help="The given season year")
    arg_parser.add_argument("-r", type=int, help="The Race Round Number of the given year")
    arg_parser.add_argument("-l", type=int, help="The Number of the Lap you want to inspect")
    arg_parser.add_argument("-v", type=str, help="Give a driver name to get according visualization")

    # Parse arguments and return accordingly
    args = arg_parser.parse_args()
    return {"year" : args.y, "race" : args.r, "lap" : args.l, "visu" : args.v}


#=====Main============================================
if __name__ == "__main__":

    # Parse the inputs
    input_dict = parse_args()

    # Get the data from API Call
    if input_dict["lap"] is None:
        race_json = get_race_data(input_dict)

        if input_dict["visu"] is None:
            output_race_data(race_json)
        else:
            plot_driver_lap_times(race_json, input_dict["visu"])
    else:
        race_json = get_lap_data(input_dict)
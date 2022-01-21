"""
    This module shall serve as web crawler for every bit of
    data we can get concerning a formula 1 race.

    Therefore we use the Formula One API grom ergast.com
    https://documenter.getpostman.com/view/11586746/SztEa7bL

    author:     Alexander Müller
    date:       15.12.2021
    version.    0.0.1

    Written for educational purposes only.
"""

#=====Imports=========================================
import json
import requests
import sys

#=====Module Imports==================================

#=====Libraries=======================================
from prettytable import PrettyTable



#=====Functions=======================================
def get_lap_data(input_dict):
    """
    Perfom a Request to the Formula One API
    with according data
    """

    # Build the URL
    search_url = f"""http://ergast.com/api/f1/{input_dict["year"]}/{input_dict["race"]}/laps/{input_dict["lap"]}.json"""
    lap_data = requests.get(url=search_url).json()
    
    print(json.dumps(lap_data, indent=4))
    return lap_data


def get_race_data(input_dict):
    """
    Perfom a Request to the Formula One API
    with according data
    """

    # Set the according file name
    file_name = f"""race_data_{input_dict["year"]}_round_{input_dict["race"]}.json"""

    # First check if the dataset is already cached in data
    try:
        with open(f"data/{file_name}") as cached_data:
            race_data = json.load(cached_data)

            print("Loading data from cache...")
            return race_data
    
    except FileNotFoundError:
        pass
    
    print("No cached data available!\nRequesting from API...")

    # Init Vars
    lap_number = 1
    bad_request = False
    race_data = {}

    # Go through  all available laps
    while not bad_request:

        search_url = f"""http://ergast.com/api/f1/{input_dict["year"]}/{input_dict["race"]}/laps/{lap_number}.json"""

        data = requests.get(url=search_url).json()
        data = data["MRData"]["RaceTable"]

        # Abort if the timing sheet is empty -> lap number not valid
        if data["Races"] == []:
            bad_request = True
            break

        # Parse the Data into the race_data
        for index, driver_set in enumerate(data["Races"][0]["Laps"][0]["Timings"]):

            if driver_set["driverId"] not in race_data.keys():
                race_data[driver_set["driverId"]] = {}

            race_data[driver_set["driverId"]][lap_number] = {
                    "time" : driver_set["time"],
                    "position" : driver_set["position"]
            }

        # Increment the lap counter
        lap_number += 1

    # Cache the found data for next time
    with open(f"data/{file_name}", "w") as output:
        output.write(json.dumps(race_data, indent=4))

    return race_data


def output_race_data(race_data):
    """
    Print a nice overview concerning the data found
    """

    # Add the needed key headers
    for driver in race_data:

        # Create a table
        table = PrettyTable()
        table.field_names = ["Lap", driver]

        # Get all lap times according to the lap
        for lap in race_data[driver]:
            table.add_row([lap, race_data[driver][lap]["time"]])

        # Give output and reset
        print(table)
        del table
    return    

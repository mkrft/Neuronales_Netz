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
import argparse


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

    # Parse arguments and return accordingly
    args = arg_parser.parse_args()
    return {"year" : args.y, "race" : args.r, "lap" : args.l}


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

    print(json.dumps(race_data, indent=4))

    return race_data

#=====Main============================================
if __name__ == "__main__":

    # Parse the inputs
    input_dict = parse_args()

    # Get the data from API Call
    if input_dict["lap"] is None:
        race_json = get_race_data(input_dict)
    else:
        race_json = get_lap_data(input_dict)

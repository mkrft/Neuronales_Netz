"""
    This is a test project to evaluate which
    f1 history data source to use for our
    AI-Race Strategy Project

    author:     Alexander Müller
    date:       13.01.2021
    version:    1.0.0

    This was created in order of our studies at
    DHBW Ravensburg-Friedrichshafen

"""

#=====Imports=========================================
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
import prettytable
import json

from src.f1_data_analyzer_helper import parse_args

#=====Main============================================
if __name__ == "__main__":

    args = parse_args()

    year = args.year
    race = args.race
    compounds = ("SOFT", "MEDIUM", "HARD")

    print(f"Year: {year}\tRound: {race} loading")

    # Define the cache to save to
    ff1.Cache.enable_cache("cache")

    # Load Session
    session = ff1.get_session(int(year), int(race), "R")
    
    # Load the Laps; only accurate ones means no SC / VSC or Red Flags
    laps = session.load_laps().pick_accurate()


    # Setup output dict
    output_data = {
        "compound" : {
            "driver" : {
                "stint" : {
                    "lap" : "data"
                }
            }
        },
        "session_info" : session.weekend.name
    }


    # Parse the data for every single driver
    for compound in compounds:

        # Add dict entry
        output_data[compound] = {}

        # Get subset of laps with certain compound
        tyre_set = laps.pick_tyre(compound)

        # Now go through every driver of the session and
        # check for their laps with the active compound
        for driver in session.drivers:
            
            driver_data = tyre_set.pick_driver(driver)

            # Setup dict
            output_data[compound][driver] = {}

            # Generate output
            print(f"\n\nDriver: {driver}\tCompund: {compound}")


            # Now gather all laps per stint to show the evoultion of the
            # laps times over tyre life span
            current_stint = 0
            for lap in driver_data.iterlaps():

                # Access all relevant data
                lap = lap[1]
                stint = int(lap["Stint"])

                # Check if the Stint has changed
                if current_stint != stint:
                    current_stint = stint
                    print(f"=======FRESH TYRES Stint: {current_stint}=======")

                # Setup dict
                if current_stint not in output_data[compound][driver]:
                    output_data[compound][driver][current_stint] = {}

                # Convert pandas timedetla to laptimes in seconds
                lap_time = float(lap["LapTime"].total_seconds())

                print(f"""{current_stint}\t{int(lap["LapNumber"])}\t{lap_time}""")

                # Save data
                output_data[compound][driver][current_stint][int(lap["LapNumber"])] = {
                    "lap_time" : lap_time
                }



    # Write everything to JSON
    with open(f"data/{year}/f1_data_{year}_{race}.json", "w") as outfile:
            json.dump(output_data, outfile, indent=4)
"""
    This is a test project to evaluate which
    f1 history data source to use for our
    AI-Race Strategy Project

    author:     Alexander Müller
    date:       13.01.2021
    version:    0.0.1

    This was created in order of our studies at
    DHBW Ravensburg-Friedrichshafen

"""

#=====Imports=========================================
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
import prettytable

#=====Main============================================
if __name__ == "__main__":

    # Set parameters
    # TODO Make this per Input params
    year = 2021
    round = 1
    compounds = ("SOFT", "MEDIUM", "HARD")

    # Define the cache to save to
    ff1.Cache.enable_cache("cache")

    # Load Session
    session = ff1.get_session(year, round, "R")
    
    # Load the Laps; only accurate ones means no SC / VSC or Red Flags
    laps = session.load_laps().pick_accurate()



    # Parse the data for every single driver
    for compound in compounds:

        tyre_set = laps.pick_tyre(compound)

        for driver in session.drivers:
            
            driver_data = tyre_set.pick_driver(driver)

            # Generate output
            print(f"\n\nDriverNr:{driver}\t{compound}")


            current_stint = 0
            for lap in driver_data.iterlaps():

                # Access all relevant data
                lap = lap[1]
                stint = lap["Stint"]

                # Check if the Stint has changed
                if current_stint != stint:
                    current_stint = stint
                    print("======FRESH TYRES======")

                print(stint, lap["LapTime"])

"""
    This module shall allow to use the gathered data to
    generate and compute strong and reliable models
    concerning the tyre degradation and their influence on the
    fastest possible lap time for each tyre in each state

    author:     Alexander Müller
    date:       08.02.2022
    version:    0.0.1

"""


#=====Imports=========================================
import os
import json

#=====Module Imports==================================

#=====Libraries=======================================


#=====Functions=======================================
def query_handler(compound, driver=None, stint=None, year=None):
    """
    Shall become a query handler, that will allow us to
    perform simple querys on the database.

    For Example to get all hard stints from 2019 that
    are longer than 10 Laps...

    param - {str} - compound - Has to be set; which tyre is of interest
    param - {int} - driver - Number of the driver, if not set all drivers
    param - {int} - stint - Number of the stint, if not set all stints
    param - {int} - year - Year of interest, if not set whole database

    return - {dict} - query_data 
    """

    # Init
    dirs = []

    # Check which files to open
    if year is not None:
        
        # Not checking if file path existing, will do further down
        dirs.append(f"data/{year}")

    else:

        # List all directories that are of interest
        for year_data in os.listdir("data/"):
            dirs.append(f"data/{year_data}")


    # Ingest whole data
    data_dict = {}

    for directory in dirs:
        for race_data_file in os.listdir(directory):
            
            with open(f"{directory}/{race_data_file}", "r") as race_data:

                # Now we have the whole data of specified year or all years
                data_dict[race_data_file] = json.load(race_data)

    # Now get rid of all data we dont want
    # Compound
    # Driver
    # Stint
        
            




#=====Main============================================
if __name__ == "__main__":

    #TODO Could add arg-parsing, but yeah

    # Perform a query
    query_handler(compound="SOFT")
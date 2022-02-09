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
import numpy

#=====Functions=======================================
def query_handler(compound, driver=None, year=None, min_stint_length=0):
    """
    Shall become a query handler, that will allow us to
    perform simple querys on the database.

    For Example to get all hard stints from 2019 that
    are longer than 10 Laps...

    param - {str} - compound - Has to be set; which tyre is of interest
    param - {int} - driver - Number of the driver, if not set all drivers
    param - {int} - year - Year of interest, if not set whole database
    param - {int} - min_stint_length - Length the stints shall have

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
    # Stint_Length
    query_data = []
    for race_file in data_dict:

        for race_compound in data_dict[race_file]:
            
            # Only bother with needed compound
            if race_compound == compound:

                # Differ is the driver is set
                # Not cleanest code due to the same functions twice, but better perfomance
                if driver is None:
                    
                    for race_driver in data_dict[race_file][race_compound]:
                        for stint in data_dict[race_file][race_compound][race_driver]:
                            
                            # Check of stint is longer than we want
                            if len(data_dict[race_file][race_compound][race_driver][stint]) >= min_stint_length:
                            
                                # Gen a new sub list for this single data
                                query_data.append([])

                                # Now append every single laptime to newst sub list of out query data
                                for lap in data_dict[race_file][race_compound][race_driver][stint]:
                                    query_data[-1].append(data_dict[race_file][race_compound][race_driver][stint][lap]["lap_time"])
                else:

                    # Go trough every single stint
                    for stint in data_dict[race_file][race_compound][str(driver)]:
                        
                        # Check of stint is longer than we want
                        if len(data_dict[race_file][race_compound][str(driver)][stint]) >= min_stint_length:
                            
                            # Gen a new sub list for this single data
                            query_data.append([])

                            # Now append every single laptime to newst sub list of out query data
                            for lap in data_dict[race_file][race_compound][str(driver)][stint]:
                                query_data[-1].append(data_dict[race_file][race_compound][str(driver)][stint][lap]["lap_time"])


    return query_data


def normalize_data(query_data):
    """
    Normalize every given stint of set from the query result
    to the reference time of 80s per lap

    For this just take the first lap of each stint and normalize it to 80s
    from there get a factor to multiple on every single other lap to get it compareable
    This eliminates circut factors, weather, driver skill and car performance

    Order of the elements must be preserved!

    param - {list[list]} - query_data - Containing our raw sets of stints following the query

    return - {list[list]} - query_data - Same structure as query_data but normalized
    """

    # Set reference_time to normalize to
    reference_time = 80

    for query_index, stint_set in enumerate(query_data):

        # Compute norm_factor from reference_time and the first lap set each stint
        # TODO Could think about using the fastest / slowest / average lap of each stint?
        norm_factor = reference_time / stint_set[0]

        # Now go through every lap and alter it according to norm factor
        for lap_index, laptime in enumerate(stint_set):

            query_data[query_index][lap_index] = round(laptime * norm_factor, 4)


    return query_data


def generate_numpy_models(query_data):
    """
    Compute a polynominal function with the help
    of numpy, degree if the polynom is changeable

    Least squares polynomial fit

    param - {list[list]} - query_data - payload

    return - {list[list]} - models
    
    """

    # Go through every stint set and gen a function
    models = []
    for stint_set in query_data:

        # Skip data sets that are too small and will raise an exception
        # Only necessary if the min_stint_length is 0
        if len(stint_set) <= 1:
            continue

        # Compute Polynom with x-axis the number of laps as a list from
        models.append(list(numpy.polyfit(list(range(0, len(stint_set))), stint_set, 2)))
        models[-1].append(len(stint_set))

    return models

#=====Main============================================
if __name__ == "__main__":

    #TODO Could add arg-parsing, but yeah
    compound = "HARD"
    year = 2021
    driver = None
    stint_length = 50

    # Perform a query
    query_data = query_handler(compound=compound, driver=driver, min_stint_length=stint_length, year=year)
    
    # Quick Info
    print(f"Found {len(query_data)} sets. Normalizing...")

    # Normalize the query to the target time of about 80 sec
    query_data_norm = normalize_data(query_data)

    # Generate functions; test with different approches and document on them -> Compare
    # First of all simple func gen on every single set and then compare the found models; average of the models
    # Single Regressions over all the data
    models = generate_numpy_models(query_data)

    print(models[0][0], models[0][1], models[0][2], models[0][3])
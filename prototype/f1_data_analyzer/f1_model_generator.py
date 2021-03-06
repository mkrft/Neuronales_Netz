"""
    This module shall allow to use the gathered data to
    generate and compute strong and reliable models
    concerning the tyre degradation and their influence on the
    fastest possible lap time for each tyre in each state

    author:     Alexander Müller
    date:       08.02.2022
    version:    1.0.0

"""

#====CONFIG==========================================
POLYNOM_POWER = 4

#=====Imports=========================================
import os
import json
import argparse
import datetime

from src.customEnums import (enTyreType,enInterpolationMode, EnumAction)

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
                    try:
                        for stint in data_dict[race_file][race_compound][str(driver)]:
                            
                            # Check of stint is longer than we want
                            if len(data_dict[race_file][race_compound][str(driver)][stint]) >= min_stint_length:
                                
                                # Gen a new sub list for this single data
                                query_data.append([])

                                # Now append every single laptime to newst sub list of out query data
                                for lap in data_dict[race_file][race_compound][str(driver)][stint]:
                                    query_data[-1].append(data_dict[race_file][race_compound][str(driver)][stint][lap]["lap_time"])
                    except KeyError:
                        raise KeyError(f"Driver {driver} not available, check out the formula 1 driver numbers on f1.com")


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
        models.append(list(numpy.polyfit(list(range(0,len(stint_set))), stint_set, POLYNOM_POWER)))
        models[-1].append(len(stint_set))

    return models


def combine_models(models, mode=enInterpolationMode.A):
    """
    Now that we have all our models, we can try to get them
    into one single model that therefore represents all of them
    
    param - {list[list]} - models - all the found models as list, inner list represent [x^POLYNOM_POWER, x^POLYNOM_POWER - 1, ..., valid_x_threshold]
    param - {str} - mode - define how you want to squash the models into one (average, median, ...)

    return - {model} - representing model of form [x^POLYNOM_POWER, x^POLYNOM_POWER - 1, ..., valid_x_threshold]
    """

    # Init
    target_model = []
    polynom_parameter_list = []

    # Go through all models
    for model in models:

        for index, parameter in enumerate(model):

            # Now save all parameters of different models in one list
            # Allowing us to get the average/median/.. of each parameter individually
            try:
                polynom_parameter_list[index].append(parameter)
            except IndexError:
                polynom_parameter_list.append([])
                polynom_parameter_list[index].append(parameter)
    
    # Now compute the single representing model
    for parameter_set in polynom_parameter_list:

        
        if mode == enInterpolationMode.A:
            target_model.append(average(parameter_set))

        elif mode == enInterpolationMode.M:
            target_model.append(median(parameter_set))

    return target_model



#=====Helpers=========================================
def print_model(model):
    """Print a instance of datatype model"""

    for index, entry in enumerate(model):
        if index == len(models[0])-1:
            print(f"xE[0,{entry}]")
            break
        print(f"x^{POLYNOM_POWER-index} * {entry}")


def average(input_set):
    """Average of a given list of int / floats"""
    return sum(input_set) / len(input_set)

def median(input_set):
    """Median of a given list of int / floats; Not the median per def but close enough because of the "len() % 2 != 0" case"""
    return sorted(input_set)[round(len(input_set)/2)]


def parse_args():
    '''Function to parse the console attribute arguments'''

    last_season_year = int(datetime.datetime.now().date().strftime("%Y")) -1

    parser = argparse.ArgumentParser()

    parser.add_argument('-y','--year',type=int,default=last_season_year)
    parser.add_argument('-d','--driver', type=str,default=None)
    parser.add_argument('-l','--length', type=int, default=30)


    parser.add_argument('-t','--tyre', type=enTyreType, action=EnumAction, help="Select Typre-Type: S-Soft, M-Medium, H-Hard", default=enTyreType.S)
    parser.add_argument('-i', '--interpolationmode', type=enInterpolationMode, action=EnumAction, help="Select the interpolation mode: A-Average, M-Median",default=enInterpolationMode.A)


    try:
        args = parser.parse_args()
    except Exception as e:
        print("Error while parsing arguments, invalid arguments given")
        exit()


    if(args.length < 5):
        print("You selected a stint with less than 30 rounds, which is the minimum value, it will be set to this value")
        args.length = 5
        # TODO think of not setting the mindistance and working with real value or throwing an exception and exiting

    return args

    

#=====Main============================================
if __name__ == "__main__":
    # Care that the stint_length must be similar to the expected tyre life otherwise the models
    # will lose validation quickly! But increasing the stint_length to much will reduce the number of fitting sets
    # drastically; therefore, as always in motorsports, we have to find a good balance!
    # But on the other hand only the long stints actually tell us about the tyre performance when it comes closer to end of tyre life
    args = parse_args()
    compound = args.tyre
    compound = compound.value[0]
    year = args.year
    driver = args.driver
    min_stint_length = args.length
    combining_mode = args.interpolationmode

    # Give short infd
    print(f"Query for:\ncompound:\t{compound}\nyear:\t\t{year}\ndriver:\t\t{driver}\nstint_length:\t{min_stint_length}\n\n")

    # Perform a query
    query_data = query_handler(compound=compound, driver=driver, min_stint_length=min_stint_length, year=year)
    print(f"Found {len(query_data)} sets. Normalizing...")

    # Normalize the query to the target time of about 80 sec
    query_data_norm = normalize_data(query_data)

    # Generate functions; test with different approches and document on them -> Compare
    # First of all simple func gen on every single set and then compare the found models; average of the models
    # Single Regressions over all the data
    print("Generating models...")
    models = generate_numpy_models(query_data)

    # Now that we have all models we can try to take a average over all the found models
    print(f"\nCombining Method: {combining_mode.value}\nResulting model:")
    average_model = combine_models(models, mode=combining_mode)

    print_model(average_model)


##### OVERALL NOTES
# The Fact I normalized to 80 Seconds means they will have laptimes slightly unter 80s, about 78-77s meaning we can
# increase the overall race distance due to being a "short" circut, this also helps concerning the fact that with only 60 laps
# as done in the prototype, the HARD would be quite nice from start to finish
#
# What i like big time about the models it the fact that the tyre warm up is shown strongly with peak performances after about 3-5 laps
#
# The models have to go towards +infinity with x going towards +infinity otherwise the tyres would be come undefinable awesome after more laps
# than they should ever be able to endure -> no need to implement penalty because its in the models themselves already
#
# Normalizing the first value means alls tyres start the first lap with 80 sec... not optimal but close enough i suppose
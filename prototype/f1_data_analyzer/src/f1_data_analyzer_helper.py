"""
    Module to hold helper functions for the f1_data_analyzer
"""

#=====Imports=========================================
import argparse
import datetime

#=====Functions=======================================


def parse_args():
    """
    Function that parses the command line arguments

    When none where given, some default values will be returned,
    default values:
        year: currentyear -1 -> year of the last complete season
        round: 1
    The return value is a complex object that holds the given arguments as directly accessible properties

    return - {obj} - args
"""
    last_season_year = int(datetime.datetime.now().date().strftime("%Y")) -1

    parser = argparse.ArgumentParser()
    parser.add_argument('-y','--year',default=last_season_year)
    parser.add_argument('-r', '--race', default=1)
    parser.add_argument('-d', '--driver', default="VER")
    args = parser.parse_args()

    return args

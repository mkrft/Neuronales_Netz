"""
    Module to compute a estimated laptime concering
    every important aspect of a car (power, driver, tyre, ...)

    The Reference Time sets the time that shall be returned if
    the power is 0.5
    the skill is 0.5
    and with fresh mediums (degredation 100%)

    TODO Add the function

"""

# TODO Remove random alteration; just here for testing
import random

#=====Module Imports==================================
from src.config import REFERANCE_LAP_TIME


#=====Functions=======================================
def compute_lap_times(car):
    """
    Compute the current lap time (pace) of a single
    car with concern to all the important data

    param - {obj} - car - Holding all information that is relevant for the computation

    return - {int} - lap_time
    """

    lap_time = REFERANCE_LAP_TIME + driver_function(car.driver.skill) + power_function(car.power) + tyre_function(car.tyre) + random.randint(1,3)

    return lap_time

def driver_function(skill):
    """
    Compute the driver influence on the laptime

    param - {float} - skill - Skill value of the driver

    return - {float} - skill_delta
    """

    return 0.0


def power_function(power):
    """
    Compute the cars power influence on the laptime

    param - {float} - power - Power value of the car

    return - {float} - power_delta
    """

    return 0.0


def tyre_function(tyre):
    """
    Compute the tyre influence on the laptime
    according to the tyre compound and degredation

    param - {obj} - tyre - Object of the class tyre, fitted to a car

    return - {float} - tyre_delta - Delta the tyre influences laptime in seconds
    """

    return 0.0

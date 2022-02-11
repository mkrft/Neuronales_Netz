"""
    Module to compute a estimated laptime concering
    every important aspect of a car (power, driver, tyre, ...)

    TODO Rework the driver and power function, those are very unscientific

"""


#=====Module Imports==================================
from src.const import (
        SOFT,
        MEDIUM,
        HARD
        )


#=====Functions=======================================
def compute_lap_times(car):
    """
    Compute the current lap time (pace) of a single
    car with concern to all the important data

    param - {obj} - car - Holding all information that is relevant for the computation

    return - {int} - lap_time
    """

    lap_time = driver_function(car.driver.skill) + power_function(car.power) + tyre_function(car.tyre)

    return round(lap_time, 2)


def driver_function(skill):
    """
    Compute the driver influence on the laptime

    param - {float} - skill - Skill value of the driver

    return - {float} - skill_delta
    """

    return round(-2*skill + 1, 2)


def power_function(power):
    """
    Compute the cars power influence on the laptime

    param - {float} - power - Power value of the car

    return - {float} - power_delta
    """

    return round(1.833333 - 3*power, 2)


def tyre_function(tyre):
    """
    Compute the tyre influence on the laptime
    according to the tyre compound and degredation

    param - {obj} - tyre - Object of the class tyre, fitted to a car

    return - {float} - tyre_delta - Delta the tyre influences laptime in seconds
    """

    x = tyre.tyre_life

    if tyre.compound == SOFT:
        return round(2.1047496 * 10**(-6) * x**(4) - 7.159884 * 10**(-6) * x**(3) + 0.00060814 * x**(2) + 0.0491257*x +76.5, 3)
    elif tyre.compound == MEDIUM:
        return round(1.134435 * x**(4) * 10**(-5) - 0.000897565 * x**(3) + 0.0184279 * x**(2) - 0.07589*x + 80, 3)
    elif tyre.compound == HARD:
        return round(2.16877 * 10**(-6) * x**(4) - 0.00033556 * x**(3) + 0.0164474 * x**(2) - 0.24907*x + 79.5745, 3)

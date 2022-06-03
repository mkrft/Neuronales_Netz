"""
    Module to compute a estimated laptime concering
    every important aspect of a car (power, driver, tyre, ...)

"""


#=====Module Imports==================================
from src.const import (
        SOFT,
        MEDIUM,
        HARD
        )
from src.cars import Car
from src.tyre import Tyre


#=====Functions=======================================
def compute_lap_times(car:Car) -> float:
    """
    Compute the current lap time (pace) of a single
    car with concern to all the important data

    param - {obj} - car - Holding all information that is relevant for the computation

    return - {int} - lap_time
    """

    lap_time = individual_performance(car.driver.skill, car.power) + tyre_function(car.tyre)

    return round(lap_time, 2)


def individual_performance(skill : float, power: float) -> float:
    """
    Compute an add on to the lap time according to the performance of the car
    and the skill of its driver

    This is based on data concerning HAM and MAZ from 2021 as biggest differences. Sorry Russia.

    param - {float} - skill
    param - {float} - power

    return - {float} - lap_time_addon
    """

    x = skill + power
    return -0.477811 * x**(4) + 2.26017 * x**(3) - 3.21407 * x**(2) + 0.51794 *x + 1.38617



def tyre_function(tyre:Tyre)->float:
    """
    Compute the tyre influence on the laptime
    according to the tyre compound and degredation

    param - {obj} - tyre - Object of the class tyre, fitted to a car

    return - {float} - tyre_delta - Delta the tyre influences laptime in seconds
    """

    x = tyre.tyre_life

    if tyre.compound == SOFT:
        return round(x**(4) * 0.00043609 - x**(3) * 0.01003 + x**(2) * 0.08299 - x*0.36458 + 79.8878, 3)
    elif tyre.compound == MEDIUM:
        return round(x**(4) * 1.58346733*10**(-5) - x**(3) * 0.00094469 + x**(2)*0.0197911 - x*0.200544 + 79.92767, 3)
    elif tyre.compound == HARD:
        return round(x**(4) * 6.08866*10**(-6) - x**(3) * 0.000321395 + x**(2)*0.005271977 - x*0.04700884 + 79.88238, 3)

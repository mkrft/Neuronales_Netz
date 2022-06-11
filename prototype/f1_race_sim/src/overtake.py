"""
    Module to handle the process of overtaking

"""

#=====Imports=========================================
import random

#=====Module Imports==================================
from src.config import OVERTAKE_TRESHOLD

#=====Functions=======================================
def check_overtake(pace_diff):
    """
    Function to determine the probability of an overtake
    and return an according bool if overtake is succesful or not

    Computation of the overtake possibility shall only based on pace. Here we chose
    simplicity and the implicity of this method rather than creating on own, hard to
    prove, model based on tyre choice, lap times, delta... because all that
    is implicit within the pace.

    param - {obj} - car - Instance of Class Car that is trying to overtake
    param - {obj} - car_infront - Instance of Class Car that is in front

    return - {bool} - overtake_done
    """

    # TODO Whole function could be a single line I think
    # It did.
    return True if random.uniform(0.0, 1.0) <= (OVERTAKE_TRESHOLD + pace_diff) else False

"""
    Class to declare and describe the behaviour
    of a tyre of different kinds

"""

#=====Imports=========================================
import random


#=====Module Imports==================================
from src.config import (
    TYRE_DEG_SOFT,
    TYRE_DEG_MEDIUM,
    TYRE_DEG_HARD,
    TYRE_INTERVAL_PENALTY
)

from src.const import (
    SOFT,
    MEDIUM,
    HARD
)

#=====Class===========================================
class Tyre():
    """
    Class to manage the many different tyres that
    will be on the different cars
    """

    def __init__(self, compound, degredation=1):
        """
        Constructor for tyres

        compound - {str} - S->Soft, M->Medium, H->Hard
        degredation - {int} - percantage of tyre health, starting at 100
        """
        self.compound = compound
        self.degredation = degredation

    #=====Property Functions Class Car=================
    @property
    def compound(self):
        return self._compound
    
    @compound.setter
    def compound(self, compound):
        self._compound = compound


    @property
    def degredation(self):
        return self._degredation
    
    @degredation.setter
    def degredation(self, degredation):
        self._degredation = degredation


    #=====Methods=====================================
    def degrade(self, car_infront=False):
        """
        Function to alter the tyre degradation over a
        single lap in clean air, meaning no car in front
        """

        # Determine which tyre is used
        if self._compound == SOFT:
            self._degredation -= round(random.uniform(TYRE_DEG_SOFT[0], TYRE_DEG_SOFT[1]), 2)
        elif self._compound == MEDIUM:
            self._degredation -= round(random.uniform(TYRE_DEG_MEDIUM[0], TYRE_DEG_MEDIUM[1]), 2)
        elif self._compound == HARD:
            self._degredation -= round(random.uniform(TYRE_DEG_HARD[0], TYRE_DEG_HARD[1]), 2)
        else:
            # TODO Add own Excpetions and according handling
            print("[Error] Tyre was not one of the three")

        # Add penalty if the car is close to a car in front
        if car_infront:
            self._degredation -= round(random.uniform(TYRE_INTERVAL_PENALTY[0], TYRE_INTERVAL_PENALTY[1]), 2)

        # Prevent tyre degredation to be negative
        if self._degredation < 0:
            self._degredation = 0.0
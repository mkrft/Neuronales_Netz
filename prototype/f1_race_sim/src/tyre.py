"""
    Class to declare and describe the behaviour
    of a tyre of different kinds

"""

#=====Imports=========================================
import random

#=====Module Imports==================================
from src.config import (
    SOFT_TYRE_LIFE,
    MEDIUM_TYRE_LIFE,
    HARD_TYRE_LIFE
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

    def __init__(self, compound, degredation=1, tyre_life=0):
        """
        Constructor for tyres

        compound - {str} - S->Soft, M->Medium, H->Hard
        degredation - {int} - percantage of tyre health, starting at 100
        """
        self.compound = compound
        self.degredation = degredation
        self.tyre_life = tyre_life

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

    @property
    def tyre_life(self):
        return self._tyre_life
    
    @tyre_life.setter
    def tyre_life(self, tyre_life):
        self._tyre_life = tyre_life


    #=====Methods=====================================
    def degrade(self, car_infront=False):
        """
        Just a simple function to display the tyre life in a percentage
        for the people viewing it!

        param - {tyre} - self
        param - {bool} - car_infront - tells you if the car is close to a car infront
        """

        # Add penalty if the car is close to a car in front
        if car_infront:
            self.tyre_life += round(random.uniform(0.03, 0.2), 2)

        # Compute the degredation level as known from F1 Games
        if self._compound == SOFT:
            self._degredation = round(1 - self.tyre_life / SOFT_TYRE_LIFE, 2)

        elif self._compound == MEDIUM:
            self._degredation = round(1 - self.tyre_life / MEDIUM_TYRE_LIFE, 2)

        elif self._compound == HARD:
            self._degredation = round(1 - self.tyre_life / HARD_TYRE_LIFE, 2)


        # Prevent tyre degredation to be negative
        if self._degredation < 0:
            self._degredation = 0.0
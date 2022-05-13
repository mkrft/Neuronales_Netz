"""
    Declaration of the Cars as own Class with the
    according attributes

    TODO Add two dry tyres rule

"""

#=====Imports=========================================
import random

#=====Module Imports==================================
from src.const import (
    SOFT,
    MEDIUM,
    HARD
)

from src.config import (
    PITSTOP_DELTA_TIME,
    PITSTOP_ERROR_RANGE
)

from src.actions import Actions
from src.tyre import Tyre 
from src.drivers import Driver
from src.customerrors import TyreNotKnownError


#=====Code============================================
class Car():
    """
        Class for easier creation of mutiple cars with different attributes
    """

    def __init__(self, driver : Driver, power:int, tyre:Tyre, position:int, race_time: float=0, last_lap_time: float=0, 
                    used_tyres : list=[], delta_to_car_infront: float=0, delta_to_leader : float = 0):
        """
        Constructor Car

        driver - {obj} - Object of Driver Class
        power - {int} - reltive to car performance
        tyre - {obj} - Object of Tyre Class
        position - {int} - Placement in the race standings
        race_time - {float} - overall time racing
        delta_to_car_infront - {float} - interval time to car infront

        """
        self.driver = driver
        self.power = power
        self.tyre = tyre
        self.position = position
        self.grid_position = position
        self.race_time = race_time
        self.last_lap_time = last_lap_time
        self.delta_to_car_infront = delta_to_car_infront
        self.delta_to_leader = delta_to_leader
        self.used_tyres = used_tyres
        self.log_info = {}

    #=====Methods=====================================
    def pitstop(self, tyre_choice : int) -> None:
        """
        Function to change tyres to a fresh set and
        add the pitstop detla time to the race time

        param - {int} - tyre_choice - correlating with the const tyre ints
        """

        # Add the Pitstop delta time to the racetime and add potential
        # time loss due to pitstop errors
        self.race_time = round(self.race_time +PITSTOP_DELTA_TIME + random.uniform(PITSTOP_ERROR_RANGE[0], PITSTOP_ERROR_RANGE[1]), 2)

        # Fit new tyre to the car
        if tyre_choice == Actions.SOFT:
            self.tyre = Tyre(SOFT)

        elif tyre_choice == Actions.MEDIUM:
            self.tyre = Tyre(MEDIUM)

        elif tyre_choice == Actions.HARD:
            self.tyre = Tyre(HARD)
        
        else:
            raise TyreNotKnownError(tyre_choice)

        # Increment number of pitstops done
        self.used_tyres.append(tyre_choice)

        return

    def distinctUsedTyreTypes(self) -> int:
        countOfUsedTypes = len(list(set(self.used_tyres)))
        return countOfUsedTypes
    

    def store_logging_data(self, lap):
        """
        Store the logging data concerning the last lap driven by self
        """

        self.log_info[f"{lap}"] = {
            "lap_time" : self.last_lap_time,
            "compound" : self.tyre.compound,
            "pos" : self.position,
            "tyre_life" : self.tyre.tyre_life
        }

    #=====Property Function Class Car=================
    
    # driver Getter/Setter
    @property
    def driver(self):
        return self._driver
    
    @driver.setter
    def driver(self, driver):
        self._driver = driver


    # tyre Getter/Setter
    @property
    def tyre(self):
        return self._tyre
    
    @tyre.setter
    def tyre(self, tyre):
        self._tyre = tyre


    # race_time Getter/Setter
    @property
    def race_time(self):
        return self._race_time
    
    @race_time.setter
    def race_time(self, race_time):
        self._race_time = race_time


    # position Getter/Setter
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        self._position = position


    # delta_to_car_infront Getter/Setter
    @property
    def delta_to_car_infront(self):
        return self._delta_to_car_infront
    
    @delta_to_car_infront.setter
    def delta_to_car_infront(self, delta_to_car_infront):
        self._delta_to_car_infront = delta_to_car_infront

    # stops Getter/Setter
    @property
    def used_tyres(self):
        return self._used_tyres
    
    @used_tyres.setter
    def used_tyres(self, used_tyres):
        self._used_tyres = used_tyres


    # grid_position Getter/Setter
    @property
    def grid_position(self):
        return self._grid_position
    
    @grid_position.setter
    def grid_position(self, grid_position):
        self._grid_position = grid_position

    #delta_to_leader Getter/Setter
    @property
    def delta_to_leader(self):
        return self._delta_to_leader

    @delta_to_leader.setter
    def delta_to_leader(self, delta_to_leader):
        self._delta_to_leader = delta_to_leader

    #last_lap_time Getter/Setter
    @property
    def last_lap_time(self):
        return self._last_lap_time

    @last_lap_time.setter
    def last_lap_time(self, last_lap_time):
        self._last_lap_time = last_lap_time
    

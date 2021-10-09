"""
    Declaration of the Cars as own Class with the
    according attributes

"""

class Car():
    """
        Class for easier creation of mutiple cars with different attributes
    """

    def __init__(self, driver, power, tyre, position, race_time, delta_to_car_infront=0):
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
        self.race_time = race_time
        self.delta_to_car_infront = delta_to_car_infront

    
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
    
    

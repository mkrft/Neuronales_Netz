"""
    Declaration of the Cars as own Class with the
    according attributes

"""

class Car():
    """
        Class for easier creation of mutiple cars with different attributes
    """

    def __init__(self, driver, power, tyre, position, race_time=0, lap=0):
        """
        Constructor Car

        driver - {obj} - Object of Driver Class
        power - {int} - from 

        """
        self.driver = driver
        self.power = power
        self.tyre = tyre
        self.position = position
        self.race_time = race_time
        self.lap = lap

    
    #=====Property Function Class Car=================
    # TODO add all functions that are needed! Only those

    @property
    def driver(self):
        return self._driver
    
    @driver.setter
    def driver(self, driver):
        self._driver = driver

    @property
    def race_time(self):
        return self._race_time
    
    @race_time.setter
    def race_time(self, race_time):
        self._race_time = race_time
    

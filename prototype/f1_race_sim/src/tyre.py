"""
    Class to declare and describe the behaviour
    of a tyre of different kinds

"""

class Tyre():
    """
    Class to manage the many different tyres that
    will be on the different cars
    """

    def __init__(self, compound, degredation=1):
        """
        Constructor for tyres

        compound - {str} - S->Soft, M->Medium, H->Hard
        degredation - {int} - percantage of tyre health, starting at 100%
        """
        self.compound = compound
        self.degredation = degredation

    #=====Property Function Class Car=================
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
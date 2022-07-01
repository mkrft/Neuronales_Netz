"""
    Declaration of the driver Class

    Every driver shall have a specific name and
    an according skill rating to mix up the field
"""

class Driver():
    """
        Class containing the definition of a driver
        in this Simulator
    """

    def __init__(self, name, short, skill):
        """
        Constructor for a driver

        name - {str} - Reperesents the Name of the driver
        short - {str} - Shall be a 3 letter string to shorten the driver names
        skill - {int} - Number from 0 to 100 describing the skill lever of the driver
        
        """

        self.name = name
        self.short = short
        self.skill = skill

    
    #=====Property Function Class Driver=================
    # TODO add all functions that are needed! Only those

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


    @property
    def skill(self):
        return self._skill
    
    @skill.setter
    def skill(self, skill):
        self._skill = skill
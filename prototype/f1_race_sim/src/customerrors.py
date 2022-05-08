
#======Module Imports========
from src.const import (
    SOFT,
    MEDIUM,
    HARD
)

#========Code===============
class RaceError(Exception):
    """
    Exception that is raised, when an error in the race occurs
    """

    def __init__(self,message:str = "An error related to the race has occured"):
        """
        Constructor RaceError

        message - {str} - Message that gives detailed information about the raceerror
        """
        self.message = message
        super().__init__(self.message)



class TyreNotKnownError(Exception):
    """
    Exception that is raised, when an unknown tyre is requested
    """

    def __init__(self,requestTyre : str,message:str=f"The available types are {SOFT}, {MEDIUM}, {HARD}"):
        """
        Constructor TyreNotKnownError

        message - {str} - Message that gives more information about the tyreerror
        """
        self.message = f"An unknown tyre of type {requestTyre} was requested. \n {message}"
        super().__init__(self.message) 
    
"""
Class (Exception) raised, when an unknown tyre is requested
"""
#=====Module Imports==================================
from src.const import (
    SOFT,
    MEDIUM,
    HARD
)

class TyreNotKnownError(Exception):
    """
    Exception that is raised, when an unknown tyre is requested
    """

    def __init__(self,requestTyre : str,message : str=f"The available types are {SOFT}, {MEDIUM}, {HARD}"):
        self.message = f"An unknown tyre of type {requestTyre} was requested. \n {message}"
        super().__init__(self.message)
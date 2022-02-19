"""
    Module to contain Enums for selecting in ArgParse

    TODO: Consider using the concept of enums as replacement for the definitions of some constant values 
    in f1_race_sim -> possibly is a concept, that is more robust and easier to extend
"""

#========Imports==============
from enum import Enum
from argparse import Action



class enTyreType(Enum):
    '''
        Enum representing all available TypreTypes for selection
    '''
    H = "HARD",
    M = "MEDIUM",
    S = "SOFT"

class enInterpolationMode(Enum):
    '''
        Enum representing all available InterpolationModes for selection
    '''
    A = "average",
    M = "median"




class EnumAction(Action):
    '''
        Class used for dynamic handling of Enums as action parameters in argparse
    '''
    def __init__(self, **kwargs):
        enumType = kwargs.pop("type",None)

        if enumType is None:
            raise ValueError("The Type must be assigned")
        if not issubclass(enumType,Enum):
            raise ValueError("The assigned type must be of type enum")

        #for referencing the values of enums as input choices in argparse change e.name to e.value
        kwargs.setdefault("choices",tuple(e.name for e in enumType))

        super(EnumAction,self).__init__(**kwargs)
        self._enum = enumType

    def __call__(self, parser, namespace, values,option_string=None):
        # for referencing the values of enums as inputs in argparse change self._enum[values] to self._enum(values)
        value = self._enum[values]
        setattr(namespace, self.dest, value)

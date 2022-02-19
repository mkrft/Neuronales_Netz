from enum import Enum
from argparse import Action

class enTyreType(Enum):
    H = "HARD",
    M = "MEDIUM",
    S = "SOFT"

class enInterpolationMode(Enum):
    A = "average",
    M = "median"




class EnumAction(Action):
    def __init__(self, **kwargs):
        enumType = kwargs.pop("type",None)

        if enumType is None:
            raise ValueError("The Type must be assigned")
        if not issubclass(enumType,Enum):
            raise ValueError("The assigned type must be of type enum")

        kwargs.setdefault("choices",tuple(e.name for e in enumType))

        super(EnumAction,self).__init__(**kwargs)
        self._enum = enumType

    def __call__(self, parser, namespace, values,option_string=None):
        value = self._enum[values]
        setattr(namespace, self.dest, value)

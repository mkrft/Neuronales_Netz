"""
    Definition of custom Enums
"""

#===== Imports =======================================
from enum import IntEnum


#==== Enums ==========================================
class Actions(IntEnum):
    NONE = 0
    SOFT = 1
    MEDIUM = 2
    HARD = 3

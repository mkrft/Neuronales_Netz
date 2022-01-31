"""
    Module to set all global Vars for the Sim that shall
    be easily adjustable and changeable.

    Please give the according names and information with
    each new variable.

"""

# Set the number of Cars and Driver you want to simulate
NUMBER_OF_COMPETITORS = 20

# Set the race distance, meaning the number of laps to drive
RACE_DISTANCE = 60

# Set the reference for a lap time in seconds
REFERANCE_LAP_TIME = 80.0

# Race Time offset due to starting in order not parallel
RACE_START_OFFSET = 0.1

# Percentage value range of tyre degreation per normal lap
TYRE_DEG_SOFT = (0.015, 0.025)
TYRE_DEG_MEDIUM = (0.01, 0.0175)
TYRE_DEG_HARD = (0.005, 0.0125)

# Value of increased tyre deg per close interval lap
TYRE_INTERVAL_PENALTY = (0.005, 0.015)

# Seconds lost during a pitstop
PITSTOP_DELTA_TIME = 22

# Describing the potential time lost due to pitstop errors
PITSTOP_ERROR_RANGE = (0.0, 1.0)

# Delta to car infront that has to be to make the overtake possible
OVERTAKE_TRESHOLD = 1.0
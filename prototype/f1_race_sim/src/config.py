"""
    Module to set all global Vars for the Sim that shall
    be easily adjustable and changeable.

    Please give the according names and information with
    each new variable.

"""

# Set the number of Cars and Driver you want to simulate
NUMBER_OF_COMPETITORS = 20

# Set the race distance, meaning the number of laps to drive
RACE_DISTANCE = 70

# Set the reference for a lap time in seconds
REFERANCE_LAP_TIME = 80.0

# Race Time offset due to starting in order not parallel
RACE_START_OFFSET = 0.1

# Tyre Lifes of the different compounds fitting to the valid ranges of the used models
# Used jsut to display the percentage values, which serve only for visual representation so
# I added ten more then the actual valid rate is to prevent us from being still fast at 100% or even more than 100%
SOFT_TYRE_LIFE = 40
MEDIUM_TYRE_LIFE = 60
HARD_TYRE_LIFE = 70


# Seconds lost during a pitstop
PITSTOP_DELTA_TIME = 18

# Describing the potential time lost due to pitstop errors
PITSTOP_ERROR_RANGE = (0.0, 1.0)

# Delta to car infront that has to be to make the overtake possible
OVERTAKE_TRESHOLD = 1.0

# Current Race Lap as global var
CURRENT_RACE_LAP = [0]

# Times how often the games shall be played
EPISODES = 10000

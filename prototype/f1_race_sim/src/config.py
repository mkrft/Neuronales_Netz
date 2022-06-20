"""
    Module to set all global Vars for the Sim that shall
    be easily adjustable and changeable.

    Please give the according names and information with
    each new variable.

"""

# Set the number of Cars and Driver you want to simulate
NUMBER_OF_COMPETITORS = 20

# Skill / Power Field Factor
# The greater this factor the closer the field as a whole is on performance
# This factor must be >= 1
SKILL_POWER_FACTOR = 1.15

# Set the race distance, meaning the number of laps to drive
RACE_DISTANCE = 70

# Set the reference for a lap time in seconds
REFERANCE_LAP_TIME = 80.0

# Race Time offset due to starting in order not parallel
RACE_START_OFFSET = 0.15

# Tyre Lifes of the different compounds fitting to the valid ranges of the used models
# Used just to display the percentage values, which serve only for visual representation so
# I added ten more then the actual valid rate is to prevent us from being still fast at 100% or even more than 100%
SOFT_TYRE_LIFE = 25
MEDIUM_TYRE_LIFE = 45
HARD_TYRE_LIFE = 50

# AI learning rate
LEARNING_RATE = 1.5 * 1e-4

# Seconds lost during a pitstop
PITSTOP_DELTA_TIME = 18

# Describing the potential time lost due to pitstop errors
PITSTOP_ERROR_RANGE = (0.0, 1.0)

# Delta to car infront that has to be to make the overtake possible
OVERTAKE_TRESHOLD = 0.25

# Current Race Lap as global var
CURRENT_RACE_LAP = [0]

# Times how often the games shall be played
EPISODES = 1000

# Maximum size of experience replay memory
MEMSIZE = 200 * RACE_DISTANCE

# Size of the batches used for learning due to experience replay
#BATCHSIZE = 1 * 70 
BATCHSIZE = 32

# Time until Epsilon reaches the minimum value
EXPLORATION_TIME = 2000

# Amount of episodes between each update for the selfplay - agent
SELFPLAY_UPDATE_INTERVAL = 500

# Path to load already trained models from
MODEL_FILE_PATH = "./models/prediction_network_weights"

# Time interval for a Network have its performance evaluated while training
NETWORK_EVALUATION_TIME = 40

# Amount of Episodes between the sampling oft the replay buffer
SAMPLING_PERIOD = 5

# AI Car Performance Values: if None than random values
# must be between [0,1] individually
AI_DRIVER_SKILL = 1
AI_CAR_POWER = 1

# AI Car Starting Position: if None than random starting position
# more of an index: So                      "0"         -> Pole
#                       "NUMBER_OF_COMPETITORS - 1"     -> last
AI_STARTING_POSITION = 0

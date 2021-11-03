"""
    Module to define and build our
    Reinforcement Learning Environment
    with OPenAI Gym.

    author:     Alexander Müller
    date:       02.11.2021
    version:    0.0.1

"""

#=====Imports=========================================

#=====Module Imports==================================
from src.const import (
    SOFT,
    MEDIUM,
    HARD
)

from src.config import (
    CURRENT_RACE_LAP,
    RACE_DISTANCE
)

from src.build_grid import build_grid

#=====Libraries=======================================
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np

#=====Functions=======================================
class RacingEnv(Env):
    """
    Our Race Environment for the RL Agent to learn in
    Parent  Env     OpenAI Gym Blueprint for an RL Environment
    """

    def __init__(self, car):
        """
        Constructor of our Env
        """

        # Define four descrete possible actions
        self.action_space = Discrete(4)

        # Arry of possibilities
        # TODO Here we will have to give a full grid state via
        # TODO a tensor or some sort
        self.observation_space = Box(low=np.array([0]), high=np.array([110]))


        # Add the according car
        self.car = car

        # Starting state
        # TODO should represent the grid from the beginning as sort of tensor?
        self.state  = car.last_lap

        
    def step(self, action):
        """
        Routine that shall be done each lap by the Agent

        param - {int} - action - Representing the four possibilities:
                                    0 - do nothing
                                    1 - pit for soft
                                    2 - pit for medium
                                    3 - pit for hard

        param - {obj} - car - Car to make the choice for
        """

        # Perform the according actions
        if action == 0:
            pass
        elif action == 1:
            self.car.pitstop(SOFT)
        elif action == 2:
            self.car.pitstop(MEDIUM)
        else:
            self.car.pitstop(HARD)

        # Give according reward per step
        # TODO
        if self.state > self.car.last_lap:
            reward = -1
        else:
            reward = 1

        # Store the last lap time to compare
        # in the next step
        self.state = self.car.last_lap
        
        # TODO Check if race is over
        if CURRENT_RACE_LAP[0] < RACE_DISTANCE - 1:
            done = False
        else:
            done = True

        # Add debug info for later
        info = {}

        return self.state, reward, done, info


    def reset(self):
        """
        Clear the grid and build a new one
        """
        
        build_grid()
        CURRENT_RACE_LAP[0] = 0

    #==Set active car=================================
    # car Getter/Setter
    @property
    def car(self):
        return self._car
    
    @car.setter
    def car(self, car):
        self._car = car
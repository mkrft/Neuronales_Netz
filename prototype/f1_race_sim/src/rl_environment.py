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
from src.get_data import get_race

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

        # limits of our state values
        float32_max = np.finfo(np.float32).max
        highs = np.array([20.0, 3.0, 1.0, float32_max , float32_max])
        lows = np.array([1.0, 0.0, 0.0, 0.0 , 0.0])
        self.observation_space = Box(low=lows, high=highs)


        # Add the according car
        self.car = car

        # Starting state
        # position, tyre.compound, car.tyre.degredation, car.race_time, car.delta_to_car_infront
        self.state = [1.0, 1.0, 1.0, 0.0, 0.0]

        
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
        if action == 1:
            self.car.pitstop(SOFT)
        elif action == 2:
            self.car.pitstop(MEDIUM)
        elif action == 3:
            self.car.pitstop(HARD)
        else:
            pass

        # Set the new state
        # self.state = self.car.tyre.degredation
        self.state = get_race(self.car)

        # Check if race is over and comupte the reward to give
        if CURRENT_RACE_LAP[0] < RACE_DISTANCE - 1:
            done = False
            reward = 0
        else:
            done = True

            if self.car.starting_pos + self.car.position == 2:
                reward = 20
            else:
                reward = -1 * self.car.position - self.car.starting_pos

        # Add debug info for later
        info = {}

        return self.state, reward, done, info


    def reset(self):
        """
        Clear the grid and build a new one
        """
        
        build_grid()
        CURRENT_RACE_LAP[0] = 0

        #Trying something
        self.state = [1.0, 1.0, 1.0, 0.0, 0.0]
        return self.state

    #==Set active car=================================
    # car Getter/Setter
    @property
    def car(self):
        return self._car
    
    @car.setter
    def car(self, car):
        self._car = car
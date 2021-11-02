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
from const import (
    SOFT,
    MEDIUM,
    HARD
)
#=====Libraries=======================================
from gym import Env
from gym.spaces import Discrete, Box
import numpy

#=====Functions=======================================
class RacingEnv(Env):
    """
    Our Race Environment for the RL Agent to learn in
    Parent  Env     OpenAI Gym Blueprint for an RL Environment
    """

    def __init__(self):
        """
        Constructor of our Env
        """

        # Define four descrete possible actions
        self.action_space = Discrete(4)

        # Arry of possibilities
        # TODO Here we will have to give a full grid state via
        # TODO a tensor or some sort
        self.observation_space = #TODO

        # Starting state
        # TODO should represent the grid from the beginning as sort of tensor?
        self.state  = #TODO

        # Add relevant car TODO may be done different
        # self.car = car

        
    def step(self, action, car):
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
            car.pitstop(SOFT)
        elif action == 2:
            car.pitstop(MEDIUM)
        else:
            car.pitstop(HARD)

        # Give according reward per step
        # TODO
        reward = 0
        
        # Check if race is over
        if current_lap != 60:
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
        pass
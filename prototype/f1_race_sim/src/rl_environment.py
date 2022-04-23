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
    RACE_DISTANCE
)

from src.build_grid import build_grid
from src.get_data import get_state
from src.cars import Car

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

    def __init__(self, car : Car):
        """
        Constructor of our Env
        """

        # Define four descrete possible actions
        self.action_space = Discrete(4)


        # limits of our state values
        float32_max = np.finfo(np.float32).max
        highs = np.array([20.0, 3.0, 1.0, float32_max , float32_max])
        lows = np.array([1.0, 0.0, 0.0, 0.0 , 0.0])
        self.observation_space = Box(low=lows, high=highs)


        # Add the according car
        self.car = car

        # previous distance to leader for per round rewards
        self.previous_delta_to_leader = 0

        # Starting state
        # position, tyre.compound, car.tyre.degredation, car.race_time, car.delta_to_car_infront
        self.state = [1.0, 1.0, 1.0, 0.0, 0.0]

        # monitoring the lost or gained time
        self.prev_state = self.state


    def update_car_params(self):
        """
        re-initialize the vars dependant on the car, avoid having to to this in the constructor.
        Making a new object every race is not needed since only the car object is modified, hence this is
        more efficient
        """
        self.starting_pos = self.car.position
        
    def step(self, action : int, lap: int):
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
        self.prev_state = self.state
        self.state = get_state(self.car)

        # Check if race is over and comupte the reward to give
        # TODO optimize the rewards
        if lap < RACE_DISTANCE - 1:
            done = False

            lost_time = self.car.delta_to_leader - self.previous_delta_to_leader

            # reward function for every round 
            reward = -0.1 * lost_time

            self.previous_delta_to_leader = self.car.delta_to_leader

        else:
            # rewards at the end of the race
            done = True

            # check the distinctness of the tyres, penalize if too low
            if(self.car.destinctUsedTyreTypes() < 2):
                reward = -1000

            if self.starting_pos + self.car.position == 2:
                reward = 200
            else:
                reward = -1 * self.car.delta_to_leader

        # Add debug info for later
        info = {}

        return self.state, reward, done, info


    def reset(self):
        """
        reset the state
        """

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

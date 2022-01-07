"""
    Module to test the race loop with the
    OpenAI Gym Environment added

"""

#=====Imports=========================================

#=====Module Imports==================================
from src.config import (
    EPISODES,
    REFERANCE_LAP_TIME,
    CURRENT_RACE_LAP,
    LEARNING_RATE,
    DISCOUNT_RATE
)

from src.const import (
    GRID_CACHE,
    SOFT,
    MEDIUM,
    HARD
)

from src.rl_environment import RacingEnv
from src.build_grid import build_grid
from src.laptime import compute_lap_times
from src.display import test_print
from src.overtake import overtaking
from src.order_grid import order_grid
from src.cars import Car
from src.tyre import Tyre

from src.keras_test import build_model
from src.agent import build_agent

#=====Libraries=======================================
from tensorflow.keras.optimizers import Adam
import numpy as np

#=====Functions=======================================
def ai_race_loop():
    """
    Main Loop representing the game
    """
    # Create the RaceEnvironment with a dummy car
    Race = RacingEnv(Car(None, None, Tyre(SOFT), None, None))

    # Dont know why the dimension of box and discrete have dissimilar getters, bit ugly
    action_size = Race.action_space.n
    observation_size = Race.observation_space.shape[0]

    # Play through the game for every episode
    for episode in range(0, EPISODES + 1):

        # Reset the game
        done = False
        score = 0
        state = Race.reset()

        # Set the active car
        Race.car = GRID_CACHE[0]

        # Race until the RACE DISTANCE is reached
        while not done:

            for car in GRID_CACHE:

                # Compute the needed lap time
                needed_lap_time = compute_lap_times(car)
                car.race_time = round(car.race_time + needed_lap_time, 2)
                car.last_lap = needed_lap_time

                # Determine if the car has increased tyre degradation or not
                # TODO add function to correlate delta with the penalty
                if car.delta_to_car_infront == "-":
                    close_car_infront = False
                elif car.delta_to_car_infront <= 1.0 and car.position != 1:
                    close_car_infront = True
                else:
                    close_car_infront = False
                
                # Let the tyre degrade according to the interval to car infront
                if close_car_infront:
                    car.tyre.degrade(car_infront=True)
                else:
                    car.tyre.degrade()

                # decide the strat for the car
                if car == Race.car:

                    pit_strat = Race.action_space.sample()
                    n_state, reward, done, info = Race.step(pit_strat)
                    score += reward
                    state = n_state

                elif CURRENT_RACE_LAP[0] == 25: 
                    car.pitstop(MEDIUM)


            # Sort the whole grid and set the accoridng intervals
            grid_sorted = order_grid()
            

            # Check for potential overtakes and let them happen
            # TODO Overtakes can still happen just by having a quicker lap...
            overtaking(grid_sorted, print_opt=False)

            grid_sorted = order_grid()

            # End active lap
            CURRENT_RACE_LAP[0] += 1

            # TODO Check if last lap and everyone has fullfilled the rule of changeing tyres at least once to different compound


        # Display the current standings
        test_print(CURRENT_RACE_LAP[0], grid_sorted)

        # Give Information about the performance of our AI
        print(f"Race: {episode}\tScore: {score}")


    # Testing some RL AI Stuff    
    # model = build_model(Race.observation_space.shape, Race.action_space.n)
    # model.summary()

    # agent = build_agent(model, Race.action_space.n)
    # agent.compile(Adam(lr=1e-3), metrics=["mae"])
    # agent.fit(Race, nb_steps=50000, visualize=False, verbose=1)



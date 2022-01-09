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

from src.agent import Agent
from src.get_data import get_race

#=====Libraries=======================================
import numpy as np
import random
import torch

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

    agent = Agent(learning_rate=0.1, inputlen=observation_size)
    # Play through the game for every episode
    for episode in range(0, EPISODES + 1):

        # Reset the game
        done = False
        score = 0
        state = Race.reset()

        agent.decay_espilon()

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
                    # depending on epsilon: explore or exploit
                    if random.uniform(0, 1) < agent.epsilon:
                        pit_strat = Race.action_space.sample()

                    else:
                        pit_strat = torch.argmax(agent.forward(torch.tensor(state,dtype=torch.float32, requires_grad=True)))

                    n_state, reward, done, info = Race.step(pit_strat)

                    # train with the data

                    agent.train_single(state, pit_strat, reward, n_state, done)
                    agent.add_replay(state, pit_strat, reward, n_state, done)

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


        agent.replay(agent.mem, 500)
        # Display the current standings
        test_print(CURRENT_RACE_LAP[0], grid_sorted)

        # Give Information about the performance of our AI
        print(f"Race: {episode}\tScore: {score}")

    weights = agent.state_dict()
    torch.save(weights, "weigts_test_file")
    
    # Testing some RL AI Stuff    
    # model = build_model(Race.observation_space.shape, Race.action_space.n)
    # model.summary()

    # agent = build_agent(model, Race.action_space.n)
    # agent.compile(Adam(lr=1e-3), metrics=["mae"])
    # agent.fit(Race, nb_steps=50000, visualize=False, verbose=1)



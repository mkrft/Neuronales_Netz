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
    SOFT,
    MEDIUM,
    HARD
)

from src.rl_environment import RacingEnv
from src.laptime import compute_lap_times
from src.display import test_print
from src.overtake import overtaking, check_overtake
from src.order_grid import order_grid
from src.build_grid import build_grid
from src.cars import Car
from src.tyre import Tyre

from src.agent import Agent

#=====Libraries=======================================
import numpy as np
import matplotlib.pyplot as plt
import random
import torch

#=====Functions=======================================
def ai_race_loop() -> None:
    """
    Main Loop representing the game
    """
    # Create the RaceEnvironment with a dummy car
    Race = RacingEnv(Car(None, None, Tyre(SOFT), None))

    # Reference for if the network is actually learning what to do: value for the actions immediately before race ends
    # test_state = torch.tensor([1.0, 1.0, 90.0, 1.0, 0.0, 2.0], dtype=torch.float32)
    test_state = torch.tensor([99.0, 1.0], dtype=torch.float32)
    testfile = open("testlog.txt", "a+")

    # Dont know why the dimension of box and discrete have dissimilar getters, bit ugly
    action_size = Race.action_space.n
    observation_size = Race.observation_space.shape[0]

    agent = Agent(learning_rate=1e-8, inputlen=observation_size)

    testrun = agent.forward(test_state)
    testfile.write(repr(testrun)+"\n")
    # Play through the game for every episode
    for episode in range(0, EPISODES + 1):

        # Reset the game
        done = False
        score = 0
        state = Race.reset()
        current_lap = 0

        agent.decay_epsilon(episode)

        # make new cars for every episode
        grid = build_grid()

        # Set the active car and re-initialize the corresponding parameters
        Race.car = grid[0]
        Race.update_car_params()

        # Race until the RACE DISTANCE is reached
        while not done:

            # reset every lap
            lap_time_car_infront = 0

            for position, car in enumerate(grid):

                # Compute the needed lap time
                calc_lap_time = compute_lap_times(car)

                # Tyre life gets increased by one lap
                car.tyre.tyre_life += 1

                # Now check if you make overtook a car by having a faster laptime, if so calc if your overtake is successful
                # If not make sure the calc_lap_time will be slower than the lap_time_car_infront so it wont be overtaken easily
                if (calc_lap_time < lap_time_car_infront) and (car.delta_to_car_infront != "-"):
                    if car.delta_to_car_infront <= abs(calc_lap_time - lap_time_car_infront):
                        
                        # Check if the current car is able to make the overtake
                        # If so just leave the times as they were
                        if check_overtake(car, grid[position - 1]):
                            #print(f"{car.driver.short} overtook {grid[position - 1].driver.short}")
                            pass

                        # If not "slow" the car down that was not able to overtake, so it stays behind
                        # TODO Check if set back is fair
                        else:
                            calc_lap_time = lap_time_car_infront + round(random.uniform(0.05, 0.5), 3)

                # Apply the new lap time to the whole race time and update the reference lap for the next car
                car.race_time = round(car.race_time + calc_lap_time, 2)
                lap_time_car_infront = calc_lap_time

                # Let the tyre degrade according to the interval to car infront
                # try / except for the car on pos 1 that has the string "-" as delta, therefore no one in front and we can degrade without penalty
                try:
                    if car.delta_to_car_infront <= 0.8:
                        car.tyre.degrade(car_infront=True)
                    else:
                        car.tyre.degrade()
                except TypeError:
                    car.tyre.degrade()

                
                # decide the strat for the car
                if car == Race.car:
                    # depending on epsilon: explore or exploit
                    if random.uniform(0, 1) < agent.epsilon:
                        pit_strat = Race.action_space.sample()

                    else:
                        # take whichever action maximizes the predicted reward
                        pit_strat = torch.argmax(agent.forward(torch.tensor(state,dtype=torch.float32, requires_grad=True)))

                    # get the environment state info
                    n_state, reward, done, info = Race.step(pit_strat, current_lap)



                    # train with the data

                    agent.train_single(state, pit_strat, reward, n_state, done)
                    agent.add_replay(state, pit_strat, reward, n_state, done)

                    score += reward
                    state = n_state

                elif current_lap == 25: 
                    car.pitstop(MEDIUM)


            # Sort the whole grid and set the accoridng intervals
            grid_sorted = order_grid(grid)

            # End active lap
            current_lap += 1

            # penalty is applied in the env, only set disqualified pos here
            if(done):
                for car in grid:
                    if(car.destinctUsedTyreTypes() < 2):
                        car.position = "DSQ"

        agent.replay(agent.mem, 500)
        # Display the current standings
        test_print(current_lap, grid_sorted)

        # logging the scores for each episode
        agent.scores.append(score)

        # Give Information about the performance of our AI
        print(f"Race: {episode}\tScore: {score}")

    testrun = agent.forward(test_state)
    testfile.write(repr(testrun)+"\n")

    testfile.close()

    scores = np.array(agent.scores)
    plt.plot(scores)
    plt.show()

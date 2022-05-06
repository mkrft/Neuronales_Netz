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
    RACE_DISTANCE,
    LEARNING_RATE
)


from src.const import (
    SOFT,
    MEDIUM,
    HARD,
    NONE
)

from src.laptime import compute_lap_times
from src.display import test_print
from src.overtake import overtaking, check_overtake
from src.order_grid import order_grid
from src.build_grid import build_grid
from src.cars import Car
from src.tyre import Tyre
from src.actions import Actions

from src.agent import Agent

#=====Libraries=======================================
import numpy as np
import matplotlib.pyplot as plt
import random
import torch
import copy

#=====Functions=======================================

def step(grid, actions, lap):
    """
    do all the cars' actions
    return the new state as the cars in the grid
    """

    initial_grid = copy.deepcopy(grid)

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

        take_action(car, actions)

    grid_sorted = order_grid(grid)
    lap += 1

    rewards = give_lap_rewards(actions, initial_grid, grid)

    if lap == RACE_DISTANCE:
        for car in grid:
             if(car.distinctUsedTyreTypes() < 2):                    
                 car.position = "DSQ"
        rewards = give_race_rewards(actions, grid)

    return grid, lap, rewards


def take_action(car, actions):
    """
    do the actions for the specified cars
    in case of no supplied action do something statically
    params:
    car - car object for which the decision is to be made
    action - dictionary mapping car objects to actions
    """
    try:
        action = actions[car]
    except KeyError:
        action = NONE

    if action == NONE:
        pass
    else:
        car.pitstop(action)


def determine_ai_action(agent, state):
    """
    Return an action 
    """
    if random.uniform(0, 1) < agent.epsilon:
        action = Actions(random.randint(0,len(Actions)-1))
    else:
        action_idx = torch.argmax(agent.forward(state))
        action = Actions(action_idx)
    
    return action


def give_lap_rewards(actions, prior_state, posterior_state):
    # map cars to their rewards
    rewards = {}

    for car in actions:
        # copied objects from prior and posterior are no longer ==, therefore check for the driver name
        driver_name = car.driver.name
        car_in_prior_state = get_car_from_driver(driver_name, prior_state)
        car_in_posterior_state = get_car_from_driver(driver_name, posterior_state)

        if (car_in_posterior_state is not None) and (car_in_prior_state is not None):
            reward = lap_reward_func(car_in_prior_state, car_in_posterior_state)
        else:
            reward = 0

        rewards[car] = reward

    return rewards


def give_race_rewards(actions, state):
    rewards = {}

    for car in actions:
        reward = race_reward_func(car, state)
        rewards[car] = reward

    return rewards


def get_car_from_driver(driver_name, car_array):
    try:
        return [car for car in car_array if car.driver.name == driver_name][0]
    except IndexError:
        return None


def lap_reward_func(previous_car_state, current_car_state):
    # rewards for each of the agents laps 
    previous_diff_to_first = previous_car_state.delta_to_leader
    current_diff_to_first = current_car_state.delta_to_leader
    lost_time = current_diff_to_first - previous_diff_to_first

    reward = -1 * lost_time

    return reward

    
def race_reward_func(car_state, grid):
    # reward given for the last round, additionaly check the 0.0 because dsq overwrites the position
    if car_state.position == 1 or car_state.delta_to_leader == 0.0:
        ordered_grid = order_grid(grid)
        delta_to_second = ordered_grid[1].delta_to_car_infront
        reward = 50 + delta_to_second
    else:
        reward = -car_state.delta_to_leader / 5
    # confuses the ai in the current version, needs a more complex input state and net architecture
    #if car_state.position == "DSQ":
        #reward = -1000
        
    return reward


def get_reset_state():
    return [100.0, RACE_DISTANCE]


def get_state(car: Car, lap : int):
    return [car.tyre.degredation * 100, RACE_DISTANCE-lap]


def ai_race_loop(load=False):
    """
    start the learning loop by initializing some parameters and jumping into the core loop
    """
    # Reference for if the network is actually learning what to do: value for the actions immediately before race ends
    test_state = torch.tensor([99.0, 1.0], dtype=torch.float32)
    testfile = open("testlog.txt", "a+")

    agent = Agent(learning_rate=LEARNING_RATE, inputlen=len(test_state), outputlen=len(Actions),load=load)

    testrun = agent.forward(test_state)
    testfile.write(repr(testrun)+"\n")

    # Play through the game for every episode
    core_race_loop(agent)

    testrun = agent.forward(test_state)
    testfile.write(repr(testrun)+"\n")

    testfile.close()

    scores = np.array(agent.scores)
    plt.plot(scores)
    plt.show()
    plt.plot(agent.losses)
    plt.show()
    torch.save(agent.prediction_dqn.state_dict(), "prediction_network_weights")


def core_race_loop(agent) -> None:
    """
    Main Loop representing the game
    """
    for episode in range(0, EPISODES + 1):

        # Reset the game
        done = False
        score = 0
        lap = 0

        agent.decay_epsilon(episode)

        # make new cars for every episode
        grid = build_grid()

        # initialize the car for the current agent
        ai_car = grid[0]
        # Initialize the actions
        actions = {}

        state = get_reset_state()
        actions[ai_car] = determine_ai_action(agent, torch.tensor(state, dtype=torch.float32))

        # play a Race and learn from it
        while lap < RACE_DISTANCE:
            # the if its the last round, set done to true
            grid, lap, rewards = step(grid, actions, lap)

            if lap == RACE_DISTANCE:
                done = True

            n_state = get_state(ai_car, lap)

            # training the ai after taking a step in the environment
            agent.train_single(state, actions[ai_car].value, rewards[ai_car], n_state, done)
            agent.add_replay(state, actions[ai_car].value, rewards[ai_car], n_state, done)

            # reset all actions from the last lap
            actions.clear()

            # find new actions
            for car in grid:
                if car == ai_car:
                    score += rewards[ai_car]
                    actions[car] = determine_ai_action(agent, torch.tensor(n_state, dtype=torch.float32))
                elif lap == 25:
                    actions[car] = MEDIUM

            state = n_state

        agent.replay(500)

        # Display the current standings
        test_print(lap, order_grid(grid))

        # logging the scores for each episode
        agent.scores.append(score)

        # Give Information about the performance of our AI
        print(f"Race: {episode}\tScore: {score}")
        print(f"Position of car : {ai_car.position}")



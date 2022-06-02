"""
    Module to test the race loop with the
    OpenAI Gym Environment added

"""

#=====Module Imports==================================
from src.config import (
    EPISODES,
    REFERANCE_LAP_TIME,
    CURRENT_RACE_LAP,
    RACE_DISTANCE,
    LEARNING_RATE,
    BATCHSIZE,
    SELFPLAY_UPDATE_INTERVAL,
    EXPLORATION_TIME
)


from src.const import (
    SOFT,
    MEDIUM,
    HARD,
    NONE
)

from src.race_step import step
from src.display import display_standings
from src.order_grid import order_grid
from src.build_grid import build_grid
from src.eval_data_logger import dump_episode_data
from src.cars import Car
from src.actions import Actions

from src.agent import Agent

#=====Libraries=======================================
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
import torch
import copy


#====== HELPERS ======================================
def determine_ai_action(agent, state):
    """
    Return an action for the Agent to take
    """
    if random.uniform(0, 1) < agent.epsilon:
        action = Actions(random.randint(0,len(Actions)-1))
    else:
        action_idx = int(torch.argmax(agent.forward(state)))
        action = Actions(action_idx)
    
    return action


def determine_other_driver_action(old_agent, state):
    """
    Return the action for all other drivers using an older version of the ai
    """
    action_idx = int(torch.argmax(old_agent.forward(state)))
    action = Actions(action_idx)

    return action

def get_reset_state():
    return torch.tensor([100.0, RACE_DISTANCE, 0.0], dtype=torch.float32)


def get_state(car: Car, lap : int):
    return torch.tensor([car.tyre.degredation * 100, RACE_DISTANCE-lap, car.delta_to_leader], dtype=torch.float32)


#===== FUNCTIONS =====================================
def ai_race_loop(load=False, log=False, selfplay=False, test=False):
    """
    Start the learning loop by initializing some parameters and jumping into the core loop
    """

    # Reference for if the network is actually learning what to do: value for the actions immediately before race ends
    test_state = torch.tensor([99.0, 1.0, 0.0], dtype=torch.float32)
    testfile = open("testlog.txt", "a+")

    # Create our agent
    agent = Agent(learning_rate=LEARNING_RATE, inputlen=len(test_state), outputlen=len(Actions),load=load)

    # Quick test run to verify
    testrun = agent.forward(test_state)
    testfile.write(repr(testrun)+"\n")

    # Play through the game for every episode
    if not test:
        core_race_loop(agent=agent, log=log, selfplay=selfplay)
    else:
        evaluation_testloop(agent=agent, log=log, selfplay=selfplay)

    testrun = agent.forward(test_state)
    testfile.write(repr(testrun)+"\n")

    testfile.close()

    # Create plot with the scores the AI managed to achieve
    font = {
        'family' : 'normal',
        'weight' : 'normal',
        'size' : 16
    }
    matplotlib.rc('font', **font)
    matplotlib.rcParams["figure.figsize"] = [30/2.54, 23/2.54]
    matplotlib.rcParams["figure.autolayout"] = True

    scores = np.array(agent.scores)
    plt.plot(scores)
    plt.title("AI - Scores")
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.show()

    if not test:
        plt.plot(agent.losses)
        plt.title("Errors")
        plt.xlabel("Learning - step")
        plt.ylabel("Loss - value (MSE)")
        plt.show()

    # Save the current weights
    torch.save(agent.prediction_dqn.state_dict(), "./models/prediction_network_weights")


def core_race_loop(agent, log, selfplay) -> None:
    """
    Main Loop representing the game
    """

    old_agent = copy.deepcopy(agent)

    for episode in range(0, EPISODES + 1):

        if episode % SELFPLAY_UPDATE_INTERVAL == 0 and selfplay:
            old_agent = copy.deepcopy(agent)

        # Reset the game
        done = False
        score = 0
        lap = 0

        agent.decay_epsilon_linear(episode)

        # make new cars for every episode
        grid = build_grid()

        # initialize the car for the current agent
        ai_car = grid[0]
        grid[0].driver.short = "DKI"

        # Initialize the actions
        actions = {}

        state = get_reset_state()
        actions[ai_car] = determine_ai_action(agent, state)

        # Play a Race and learn from it
        while lap < RACE_DISTANCE:
            # the if its the last round, set done to true
            grid, lap, rewards = step(grid, actions, lap, log)

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
                    actions[car] = determine_ai_action(agent, n_state)

                # competitor - actions
                elif selfplay:
                    # use older version of AI - agent
                    actions[car] = determine_other_driver_action(old_agent, n_state)

                elif lap == 15:
                    # static action
                    actions[car] = Actions.MEDIUM

            state = n_state

        # learn from experiences in short term memory
        agent.replay(BATCHSIZE)

        # Display the current standings of finished episode
        display_standings(lap, order_grid(grid))

        # logging the scores for each episode
        agent.scores.append(score)

        # Give Information about the performance of our AI
        print(f"Race: {episode}\tScore: {score}")
        print(f"Position of car : {ai_car.position}")

        if log:
            dump_episode_data(grid, episode)



def evaluation_testloop(agent, log, selfplay):
    """
    Pretty much the same as the core loop, except without the learning.
    """

    old_agent = copy.deepcopy(agent)

    for episode in range(0, EPISODES + 1):

        if episode % SELFPLAY_UPDATE_INTERVAL == 0:
            old_agent = copy.deepcopy(agent)

        # Reset the game
        score = 0
        lap = 0

        # make new cars for every episode
        grid = build_grid()

        # initialize the car for the current agent
        ai_car = grid[0]
        grid[0].driver.short = "DKI"

        # Initialize the actions
        actions = {}

        state = get_reset_state()
        actions[ai_car] = determine_ai_action(agent, state)

        # play a Race and learn from it
        while lap < RACE_DISTANCE:
            # the if its the last round, set done to true
            grid, lap, rewards = step(grid, actions, lap, log)

            n_state = get_state(ai_car, lap)

            # reset all actions from the last lap
            actions.clear()

            # find new actions
            for car in grid:
                if car == ai_car:
                    score += rewards[ai_car]
                    actions[car] = determine_ai_action(agent, n_state)

                # competitor - actions
                elif selfplay:
                    # use older version of AI - agent
                    actions[car] = determine_other_driver_action(old_agentn_state)

                elif lap == 25:
                    # static action
                    actions[car] = Actions.MEDIUM

            state = n_state

        # Display the current standings of finished episode
        display_standings(lap, order_grid(grid))

        # logging the scores for each episode
        agent.scores.append(score)

        # Give Information about the performance of our AI
        print(f"Race: {episode}\tScore: {score}")
        print(f"Position of car : {ai_car.position}")

        if log:
            dump_episode_data(grid, episode)

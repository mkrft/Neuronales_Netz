"""
    Module to test the race loop with the
    OpenAI Gym Environment added

"""

#=====Module Imports==================================
from src.config import (
    EPISODES,
    CURRENT_RACE_LAP,
    RACE_DISTANCE,
    LEARNING_RATE,
    BATCHSIZE,
    SELFPLAY_UPDATE_INTERVAL,
    EXPLORATION_TIME,
    NETWORK_EVALUATION_TIME,
    SAMPLING_PERIOD,
    AI_CAR_POWER,
    AI_DRIVER_SKILL,
    AI_STARTING_POSITION
)

from src.ai_race_loop_helpers import (
    get_reset_state,
    determine_ai_action,
    get_state,
    create_plot,
    create_histogram
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
import torch
import copy
import time
import random
from pathlib import Path


#===== FUNCTIONS =====================================
def ai_race_loop(load=False, log=False, selfplay=False, test=False, mutate=False):
    """
    Start the learning loop by initializing some parameters and jumping into the core loop
    """

    # Reference for if the network is actually learning what to do: value for the actions immediately before race ends
    test_state = torch.tensor([99.0, 69.0, 0.0, 70.0, 1, 0, 1, 0, 1, 0, 1], dtype=torch.float32)
    try:
        testfile = open("./logs/testlog.txt", "a+")
    except FileNotFoundError:
        try:
            testfile = open("./logs/testlog.txt","w+")
        except FileNotFoundError:
            Path("./logs").mkdir(parents=True,exist_ok=True)
            testfile = open("./logs/testlog.txt","w+")

    # Create our agent
    agent = Agent(learning_rate=LEARNING_RATE, inputlen=len(test_state), outputlen=len(Actions),load=load,mutate=mutate)
    print("initializing replay memory with random actions . . .")
    if not test:
        agent.randomly_fill_memory()

    # Quick test run to verify
    testrun = agent.forward(test_state)
    testfile.write(repr(testrun)+"\n")
    if not test:
        core_race_loop(agent=agent, log=log, selfplay=selfplay)
    else:
        evaluation_testloop(agent=agent, log=log, selfplay=selfplay)

    testrun = agent.forward(test_state)
    testfile.write(repr(testrun)+"\n")

    testfile.close()

    create_plot(agent.scores, agent.losses, test)

    # Save the current weights
    torch.save(agent.prediction_dqn.state_dict(), "./models/prediction_network_weights")


def core_race_loop(agent, log, selfplay) -> None:
    """
    Main Loop representing the game
    """

    old_net = copy.deepcopy(agent.prediction_dqn)
    mean_score = 0

    current_best_ai = copy.deepcopy(agent.prediction_dqn)
    current_best_score = -1000000   # any very small number to ensure that better ais get saved

    for episode in range(0, EPISODES + 1):

        if episode % SELFPLAY_UPDATE_INTERVAL == 0 and selfplay:
            old_net = copy.deepcopy(agent.prediction_dqn)

        # Reset the game
        done = False
        score = 0
        lap = 1

        agent.decay_epsilon_linear(episode)
        agent.decay_temperature()

        # make new cars for every episode
        grid = build_grid()

        # Initialize the car for the current agent based on random start position
        if AI_STARTING_POSITION is None:
            startindex = random.randrange(0,len(grid))
            ai_car = grid[startindex]
        else:
            ai_car = grid[AI_STARTING_POSITION]

        ai_car.driver.short = "DKI"

        # Set AI Car Performance Parameters if needed, based on config params! Otherwise it stays
        if AI_CAR_POWER is not None:
            ai_car.power = AI_CAR_POWER

        if AI_DRIVER_SKILL is not None:
            ai_car.driver.skill = AI_DRIVER_SKILL

        # Initialize the actions
        actions = {}

        state = get_reset_state()
        actions[ai_car] = determine_ai_action(agent, state, epsilon_policy=True)

        # Play a Race and learn from it
        while lap < RACE_DISTANCE:
            # the if its the last round, set done to true
            grid, lap, rewards = step(grid, actions, lap, log)

            if lap == RACE_DISTANCE:
                done = True

            n_state = get_state(ai_car, lap)

            # training the ai after taking a step in the environment
            #agent.train_single(state, torch.tensor(actions[ai_car].value), torch.tensor(rewards[ai_car]), n_state, torch.tensor(done))
            agent.add_replay(state, torch.tensor(actions[ai_car].value), torch.tensor(rewards[ai_car]), n_state, torch.tensor(done))
            if lap % SAMPLING_PERIOD == 0:
                #agent.replay(BATCHSIZE, episode)
                agent.train_batch(BATCHSIZE)

            # reset all actions from the last lap
            actions.clear()

            # find new actions
            for car in grid:
                if car == ai_car:
                    score += rewards[ai_car]
                    actions[car] = determine_ai_action(agent, n_state, epsilon_policy=True)

                # competitor - actions
                elif selfplay:
                    # use older version of AI - agent
                    actions[car] = determine_other_driver_action(old_net, n_state)

                # static action
                elif lap == 15 and not selfplay:
                    actions[car] = Actions.MEDIUM
                    
                elif lap == 48 and not selfplay:
                    actions[car] = Actions.MEDIUM

            state = n_state

        # update the mean score
        mean_score += score

        if episode % NETWORK_EVALUATION_TIME == 0 and episode != 0:
            mean_score = mean_score / NETWORK_EVALUATION_TIME
            if mean_score >= current_best_score:
                current_best_score = mean_score
                current_best_ai = copy.deepcopy(agent.prediction_dqn)
            mean_score = 0

        # learn from experiences in short term memory
        #agent.train_batch(BATCHSIZE)
        #agent.replay(BATCHSIZE, episode)

        # Display the current standings of finished episode
        display_standings(lap, order_grid(grid))

        # logging the scores for each episode
        agent.scores.append(score)

        # Give Information about the performance of our AI
        print(f"Race: {episode}\tScore: {score}")
        print(f"Position of car : {ai_car.position}")

        if log:
            dump_episode_data(grid, episode)

    agent.prediction_dqn = current_best_ai



def evaluation_testloop(agent, log, selfplay):
    """
    Pretty much the same as the core loop, except without the learning.
    """

    old_net = copy.deepcopy(agent.prediction_dqn)

    car_positions = []

    for episode in range(0, EPISODES + 1):

        if episode % SELFPLAY_UPDATE_INTERVAL == 0:
            old_net = copy.deepcopy(agent.prediction_dqn)

        # Reset the game
        score = 0
        lap = 1

        # make new cars for every episode
        grid = build_grid()

        # Initialize the car for the current agent based on random start position
        if AI_STARTING_POSITION is None:
            startindex = random.randrange(0,len(grid))
            ai_car = grid[startindex]
        else:
            ai_car = grid[AI_STARTING_POSITION]

        ai_car.driver.short = "DKI"

        # Set AI Car Performance Parameters if needed, based on config params! Otherwise it stays
        if AI_CAR_POWER is not None:
            ai_car.power = AI_CAR_POWER

        if AI_DRIVER_SKILL is not None:
            ai_car.driver.skill = AI_DRIVER_SKILL


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
                    actions[car] = determine_other_driver_action(old_net, n_state)

                # static action
                elif lap == 15 and not selfplay:
                    actions[car] = Actions.MEDIUM

                elif lap == 48 and not selfplay:
                    actions[car] = Actions.MEDIUM

            state = n_state

        # Display the current standings of finished episode
        display_standings(lap, order_grid(grid))

        # logging the scores for each episode
        agent.scores.append(score)

        # Give Information about the performance of our AI
        print(f"Race: {episode}\tScore: {score}")
        print(f"Position of car : {ai_car.position}")

        # Add car positon to list over all episodes for histogram
        car_positions.append(ai_car.position)

        if log:
            dump_episode_data(grid, episode)

    create_histogram(car_positions)
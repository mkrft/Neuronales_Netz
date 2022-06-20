from src.config import (
    RACE_DISTANCE,
    REFERANCE_LAP_TIME)

from src.const import(
    SOFT,
    MEDIUM,
    HARD
)

from src.actions import Actions
from src.cars import Car


import torch
import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#====== HELPERS ======================================
def determine_ai_action(agent, state, epsilon_policy = True):
    """
    Return an action for the Agent to take according to the specified policy
    """
    if epsilon_policy:
        if random.uniform(0, 1) < agent.epsilon:
            action = Actions(random.randint(0,len(Actions)-1))
        else:
            action_idx = int(torch.argmax(agent.forward(state)))
            action = Actions(action_idx)

    else:
        # boltzmann policy
        softmax_layer = torch.nn.Softmax(dim=-1)
        q_vals = agent.forward(state)
        # normalize the outputs so the softmax output doesnt explode
        q_vals = q_vals.clamp(-30, 30)
        probabilities = softmax_layer(q_vals / agent.temperature)
        probabilities = probabilities.detach().numpy()
        choices = list(range(len(Actions)))
        action_idx = np.random.choice(choices, p = probabilities)
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
    degredation = 100.0
    current_lap = 1
    delta_to_leader = 0.0
    lap_time = REFERANCE_LAP_TIME
    position = 1
    soft, medium, hard = 1, 0, 1
    second_compound_flag = 0
    delta_to_front = 0
    starting_pos = 1

    return torch.tensor([degredation, current_lap, delta_to_leader, lap_time, position, soft, medium, hard, second_compound_flag, delta_to_front, starting_pos], dtype=torch.float32)


def one_hot_compound(compound):
    """
    one - hot code the current tyre type
    """
    if compound == SOFT:
        return 1, 0, 0
    elif compound == MEDIUM:
        return 0, 1, 0
    elif compound == HARD:
        return 0, 0, 1


def get_state(car: Car, lap : int):
    """
    return the current state for the AI - Input
    """
    degredation = car.tyre.degredation * 100
    current_lap = lap
    delta_to_leader = car.delta_to_leader
    lap_time = car.last_lap_time
    position = car.position
    soft, medium, hard = one_hot_compound(car.tyre.compound)
    second_compound_flag = 1 if car.distinctUsedTyreTypes() >= 2 else 0
    delta_to_front = car.delta_to_car_infront if car.delta_to_car_infront != "-" else 0
    starting_pos = car.grid_position
    state_tensor = torch.tensor([degredation, current_lap, delta_to_leader, lap_time, position, soft, medium, hard, second_compound_flag, delta_to_front, starting_pos], dtype=torch.float32)

    return state_tensor


def create_plot(scores:list,losses:list, test:bool):
    # Create plot with the scores the AI managed to achieve
    font = {
        'family' : 'normal',
        'weight' : 'normal',
        'size' : 16
    }
    matplotlib.rc('font', **font)
    matplotlib.rcParams["figure.figsize"] = [30/2.54, 23/2.54]
    matplotlib.rcParams["figure.autolayout"] = True

    scores = np.array(scores)
    plt.plot(scores)
    plt.title("AI - Scores")
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.show()

    if not test:
        plt.plot(losses)
        plt.title("Errors")
        plt.xlabel("Learning - step")
        plt.ylabel("Loss - value (MSE)")
        plt.show()


def create_histogram(values: list, bins : list):
    plt.hist(values,bins=bins, density=True)
    plt.show()

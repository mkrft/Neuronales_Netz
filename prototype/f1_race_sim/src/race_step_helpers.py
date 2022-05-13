"""
    All needed helpers for the race step (lap)
"""

#==== IMPORTS ========================================
from src.order_grid import order_grid
from src.actions import Actions


#===== HELPERS =======================================
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
        action = Actions.NONE

    if action == Actions.NONE:
        pass
    else:
        car.pitstop(action)


def give_lap_rewards(actions, prior_state, posterior_state):
    """
    Map cars to their rewards

    param - {dict} - actions - holds all the actions per car per lap
    param - {} - prior_state - 
    param - {} - posterior_state -

    return - {dict} - rewards
    """

    # Init
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
    """
    TODO
    """
    rewards = {}

    for car in actions:
        reward = race_reward_func(car, state)
        rewards[car] = reward

    return rewards


def get_car_from_driver(driver_name, car_array):
    """
    TODO
    """
    try:
        return [car for car in car_array if car.driver.name == driver_name][0]
    except IndexError:
        return None


def lap_reward_func(previous_car_state, current_car_state):
    """
    TODO
    """

    # rewards for each of the agents laps 
    previous_diff_to_first = previous_car_state.delta_to_leader
    current_diff_to_first = current_car_state.delta_to_leader
    lost_time = current_diff_to_first - previous_diff_to_first

    reward = -1 * lost_time

    return reward

    
def race_reward_func(car_state, grid):
    """
    TODO
    """

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

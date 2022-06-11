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


def clamp(val, lower, upper):
    return min(upper, max(lower, val))

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


def give_race_rewards(actions, grid):
    """
    CMap race rewards to each car
    
    param - {dict} - actions - holds all the actions per car per lap
    parma - {vec} - state - ()

    return - {dict} - rewards - per car
    """
    rewards = {}

    for car in actions:
        reward = race_reward_func(car, grid)
        rewards[car] = reward

    return rewards


def get_car_from_driver(driver_name, car_array):
    """
    Map Car Instance to driver_names

    param - {str} - driver_name
    param - {list} - car_array - list of relevant Car instances
    """
    try:
        return [car for car in car_array if car.driver.name == driver_name][0]
    except IndexError:
        return None


def lap_reward_func(previous_car_state, current_car_state):
    """
    Compute the reward for each of the agents laps 

    param - {vec} - previous_car_state
    param - {vec} - current_car_state

    return - {float} - reward
    """

    # every lap thats not the finishing one has a reward of 0
    return 0

    
def race_reward_func(car, grid):
    """
    Calc the race rewards for individual car given current grid

    param - {obj} - car - Instance of Car that it on the grid
    parma - {list} - grid

    return - {float} - reward
    """


    # confuses the ai in the current version, needs a more complex input state and net architecture
    #if car.position == "DSQ":
        #reward = -1000.0

    if car.position == 1 or car.delta_to_leader == 0.0:
        ordered_grid = order_grid(grid)
        dist_to_second = ordered_grid[1].delta_to_car_infront
        reward = dist_to_second / 100
    elif car.position == 'DSQ':
        ordered_grid = order_grid(grid)
        pos = ordered_grid.index(car)
        reward = 1 - (pos)
    else:
        reward = (1 - car.position)
        
    return reward

# from src.build_grid import build_grid
# from src.race import race_loop
# output.add_row([car.position, car.driver.short, f"{car.tyre.compound} {round(car.tyre.degredation * 100, 2)}%", car.race_time, f"+ {car.delta_to_car_infront}"])

from src.const import GRID_CACHE
from src.config import NUMBER_OF_COMPETITORS
from src.build_grid import build_grid
from src.race import race_loop

#=====Functions=======================================
def get_race():

    build_grid()

    all_data = race_loop(False)

    return transform_data(all_data)

def make_input_vector(all_data, lap, driver_num):
    try:
        lap_data = all_data[lap-1]

    except IndexError:
        print("invalid lap for input vector, defaulting to first!")
        lap_data = all_data[0]

    # TODO evaluate if this is the proper way to tell the AI which car it is taking controll of

    if driver_num > 0 and driver_num <= NUMBER_OF_COMPETITORS:
        lap_data.append(driver_num)

    else: 
        print("invalid driver-number, defaulting to 1")
        lap_data.append(1)
    
    return lap_data


def convert_delta(delta):
    if delta == '-':
        return 0
    return delta

def convert_compound(tyre_compound):
    if tyre_compound == 'S':
        return 0.0
    if tyre_compound == 'M':
        return 1.0
    return 2.0

def convert_driver_short(driver_short):
    return float(driver_short[1:])

def transform_data(racedata): 
    """
    pytorch needs an array of values; hence turn the car - objects into usable data (numbers)
    """

    total_race_state= []
    for lap, data in enumerate(racedata):
        # TODO refine which parts of the total gamestate we actually need
        race_state_per_lap = [[i.position, convert_driver_short(i.driver.short), convert_compound(i.tyre.compound), i.tyre.degredation, i.race_time, convert_delta(i.delta_to_car_infront)] for i in data]
        race_state_per_lap = [j for i in race_state_per_lap for j in i]     # flatten the list
        race_state_per_lap.insert(0, lap)   # lap in front 
        print(race_state_per_lap)
        print(f"Neuron count in input layer for the environment : {len(race_state_per_lap)}")
        total_race_state.append(race_state_per_lap)

    return total_race_state

    
if __name__ == "__main__":
    get_race()
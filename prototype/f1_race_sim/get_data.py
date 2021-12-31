# from src.build_grid import build_grid
# from src.race import race_loop
# output.add_row([car.position, car.driver.short, f"{car.tyre.compound} {round(car.tyre.degredation * 100, 2)}%", car.race_time, f"+ {car.delta_to_car_infront}"])

from src.const import GRID_CACHE
from src.build_grid import build_grid
from src.race import race_loop

#=====Functions=======================================
def get_race():

    build_grid()

    all_data = race_loop(False)

    return transform_data(all_data)



def transform_data(racedata): 
    """
    pytorch needs an array of values; hence turn the car - objects into usable data
    """

    total_race_state= []
    for lap, data in enumerate(racedata):
        # TODO refine which parts of the total gamestate we actually need
        # TODO somehow convert these all to numbers and find a way to build a model that makes sense
        race_state_per_lap = [[i.position, i.driver.short, i.tyre.compound, i.tyre.degredation, i.race_time, i.delta_to_car_infront] for i in data]
        race_state_per_lap = [j for i in race_state_per_lap for j in i]
        race_state_per_lap.insert(0, lap) # lap at first index
        print(race_state_per_lap)
        print(f"Neuron count in input layer for the environment : {len(race_state_per_lap)}")
        total_race_state.append(race_state_per_lap)


    return total_race_state

    
    
if __name__ == "__main__":
    get_race()

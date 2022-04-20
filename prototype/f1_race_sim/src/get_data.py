from src.config import NUMBER_OF_COMPETITORS
from src.build_grid import build_grid
from src.race import race_loop

#=====Functions=======================================
def get_state(car):
    return [car.position, convert_compound(car.tyre.compound), car.tyre.degredation, car.race_time, convert_delta(car.delta_to_car_infront)]


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


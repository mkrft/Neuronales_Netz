from src.config import NUMBER_OF_COMPETITORS, RACE_DISTANCE
from src.build_grid import build_grid
from src.race import race_loop
from src.cars import Car

#=====Functions=======================================
def get_state(car : Car, lap : int):
    #return [car.position, convert_compound(car.tyre.compound), car.tyre.degredation * 100 , RACE_DISTANCE - lap, convert_delta(car.delta_to_car_infront), car.destinctUsedTyreTypes()]
    return [car.tyre.degredation * 100, RACE_DISTANCE-lap]


def convert_delta(delta) -> float:
    if delta == '-':
        return 0
    return delta


def convert_compound(tyre_compound :str) -> float:
    if tyre_compound == 'S':
        return 0.0
    if tyre_compound == 'M':
        return 1.0
    return 2.0


def convert_driver_short(driver_short) -> float:
    return float(driver_short[1:])


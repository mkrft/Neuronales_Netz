"""
    F1 Race Simulator

    This Project follows the ambition to simulate
    the timeing sheets of a full formula one race
    with concern to tyre degradation.

    author:     Alexander Müller
    date:       05.10.2021
    version:    0.0.1

    Please contact us for further information via Git.

"""

#=====Imports=========================================

#=====Module Imports==================================
from src.build_grid import build_grid
from src.race import race_loop

#=====Libraries=======================================

#=====Program Entry===================================
if __name__ == "__main__":

    # Init cars with drivers
    grid = build_grid()

    # Simulate race
    race_loop(grid)
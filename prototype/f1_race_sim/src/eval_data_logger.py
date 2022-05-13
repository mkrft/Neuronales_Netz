"""
    Module to create the logs from the different races
"""

#===== IMPORTS =======================================
import json

#===== FUNCTIONS =====================================
def dump_episode_data(grid, episode):
    """
    Dump the whole grid data of a single episode into a JSON

    param - {list} - grid 
    """

    # Init
    episode_data = {}

    # Copy data from every single car
    for car in grid:
        episode_data[f"{car.driver.short}"] = car.log_info

    # Write to file
    with open(f"test_epi_{episode}_log.json", "w") as log_file:
        json.dump(episode_data, log_file, indent=4)

    
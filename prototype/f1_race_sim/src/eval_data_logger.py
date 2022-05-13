"""
    Module to create the logs from the different races
"""

#===== IMPORTS =======================================
import json
import datetime
from pathlib import Path

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

    # Get current time
    time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    # Prep needed strings
    dir_name = f"logs_{time_str}"
    file_name = f"log_{time_str}_episode_{episode}"

    # Generate the new directory
    Path(f"./logs/{dir_name}").mkdir(parents=True, exist_ok=True)

    # Write to file
    with open(f"./logs/{dir_name}/{file_name}.json", "w") as log_file:
        json.dump(episode_data, log_file, indent=4)

    
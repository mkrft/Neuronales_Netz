"""
    Plotter to generate plots concerning the AI Evaluation

    author:     Alexander Mueller
    date:       14.05.2022
    version:    0.0.1

    Project: Formula One Strategy AI (FOSA)
"""

#===== IMPORTS =======================================
import argparse
import json

#===== LIBRARYS ======================================
import matplotlib.pyplot as plt
from fastf1 import plotting


#===== MAIN ========================================== 
if __name__ == "__main__":

    # Define args parser
    parser = argparse.ArgumentParser(description="Plotting parameters")
    parser.add_argument('-d','--driver', help="Driver to evaluate", required=True)
    parser.add_argument('-f', '--file', help="Log file to gather data from", required=True)
    args = parser.parse_args()

    # Read input
    driver = args.driver
    file_name = args.file

    # Read data
    with open(f"{file_name}", "r") as database:
        log_data = json.load(database)

    # Open lists
    lap_time = []
    tyre_life = []
    compound = []
    position = []
    delta_to_leader = []
    laps = []

    # Parse the data
    for lap in log_data[driver]:

        laps.append(int(lap))
        lap_time.append(log_data[driver][lap]["lap_time"])
        tyre_life.append(log_data[driver][lap]["tyre_life"])
        compound.append(log_data[driver][lap]["compound"])
        position.append(log_data[driver][lap]["pos"])
        delta_to_leader.append(log_data[driver][lap]["delta_to_leader"])

    # Make the plot
    plotting.setup_mpl()

    # Gen subplots
    fix, ax = plt.subplots(3)
    ax[0].plot(laps, lap_time, color="green")
    ax[0].set_xlabel("Laps")
    ax[0].set_ylabel("Lap Time [s]")

    ## Stint / Compound
    ax10 = ax[1].twinx()
    ax[1].plot(laps, compound, color="cyan")
    ax[1].set_xlabel("Laps")
    ax[1].set_ylabel("Compound", color="cyan")

    ax10.plot(laps, tyre_life, color="red")
    ax10.set_xlabel("Laps")
    ax10.set_ylabel("\nTire Age [Laps]", color="red")

    ## TyreLife
    ax[2].plot(laps, delta_to_leader, color="yellow")
    ax[2].set_xlabel("Laps")
    ax[2].set_ylabel("Delta to Leader [s]")

    plt.tight_layout()
    plt.show()

    


"""
    This is a test project to evaluate which
    f1 history data source to use for our
    AI-Race Strategy Project

    author:     Alexander Müller
    date:       13.01.2021
    version:    0.0.1

    This was created in order of our studies at
    DHBW Ravensburg-Friedrichshafen

"""

#=====Imports=========================================
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
import prettytable

#=====Main============================================
if __name__ == "__main__":

    # Parse input parameters
    #TODO

    # Define the cache to save to
    ff1.Cache.enable_cache("cache")

    # Setup plotting
    plotting.setup_mpl()

    # Load the laps from the race
    laps = ff1.get_session(2021, 1, "R").load_laps()

    # Get desired driver
    vettel = laps.pick_driver("VER")

    # Gen a Plot
    fix, ax = plt.subplots(3)
    ax[0].plot(vettel["LapNumber"], vettel["LapTime"], color="green")
    ax[0].set_xlabel("Lap Number")
    ax[0].set_ylabel("Lap Time")

    ax[1].plot(vettel["LapNumber"], vettel["Compound"], color="cyan")
    ax[1].set_xlabel("Lap Number")
    ax[1].set_ylabel("Tyre")

    ax[2].plot(vettel["LapNumber"], vettel["Stint"], color="red")
    ax[2].set_xlabel("Lap Number")
    ax[2].set_ylabel("Stint")
    plt.show()

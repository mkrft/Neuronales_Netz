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

#=====Library Imports=================================
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
import prettytable

#=====Module Imports==================================
from src.f1_data_analyzer_helper import parse_args


#=====Main============================================
if __name__ == "__main__":

    # Parse input parameters
    args = parse_args()
    year = args.year
    race = args.race
    driver = args.driver

    # Define the cache to save to
    ff1.Cache.enable_cache("cache")

    # Setup plotting
    plotting.setup_mpl()

    # Load the laps from the race
    laps = ff1.get_session(year, race, "R").load_laps()

    # Get desired driver
    driver = laps.pick_driver(driver)

    # Convert the lap times to seconds
    lap_times = []
    for lap in driver.iterlaps():
        lap = lap[1]
        lap_times.append(lap["LapTime"].total_seconds())

    # Gen Plot
    ## Laptimes
    # TODO add y-scale limits based on average laptime +- 1sec
    fix, ax = plt.subplots(3)
    ax[0].plot(driver["LapNumber"], lap_times, color="green")
    ax[0].set_xlabel("Lap Number", fontsize=15)
    ax[0].set_ylabel("Lap Time in Seconds", fontsize=15)

    ## Stint / Compound
    ax10 = ax[1].twinx()
    ax[1].plot(driver["LapNumber"], driver["Compound"], color="cyan")
    ax[1].set_xlabel("Lap Number", fontsize=15)
    ax[1].set_ylabel("Compound", color="cyan", fontsize=15)

    ax10.plot(driver["LapNumber"], driver["Stint"], color="red")
    ax10.set_xlabel("Lap Number", fontsize=15)
    ax10.set_ylabel("\nStint", color="red", fontsize=15)

    ## TyreLife
    ax[2].plot(driver["LapNumber"], driver["TyreLife"], color="yellow")
    ax[2].set_xlabel("Lap Number", fontsize=15)
    ax[2].set_ylabel("TyreLife in Rounds", fontsize=15)

    # To get a window in full size
    mng = plt.get_current_fig_manager()
    #mng.window.showMaximized()

    mng.set_window_title(f"Race Data {year} {race} {driver}")

    # Show
    plt.tight_layout()
    plt.show()

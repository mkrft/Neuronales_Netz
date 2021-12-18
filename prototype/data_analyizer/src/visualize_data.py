"""
    Create plots concerning the found data

"""

#=====Imports=========================================

#=====Module Imports==================================
from src.convert_time import convert_time

#=====Libraries=======================================
import matplotlib.pyplot as plt

#=====Functions=======================================
def plot_driver_lap_times(race_data, driver_name):
    """
    Give a neat plot concerning the lap_times of this driver

    param - {dict} - race_data
    param - {str} - driver_name
    """

    # Parse lap times as list
    lap_times = []
    laps = []
    if driver_name in race_data.keys():
        for lap in race_data[driver_name]:

            # Translate time string into seconds
            lap_time = convert_time(race_data[driver_name][lap]["time"])
            
            lap_times.append(lap_time)
            laps.append(int(lap))
    
    else:
        driver_name = input(f"Driver Name not matching. Please insert one of the following:\n{race_data.keys()}\n")
        plot_driver_lap_times(race_data, driver_name)
        return

    # Create plot
    plt.plot(laps, lap_times)
    plt.show()

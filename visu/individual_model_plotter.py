"""
Quick Plotter to generate Matplotlib plots of our models

    author:     Alexander Müller
    date:       31.05.2022
    version:    0.0.1

"""

#===== Imports =======================================
from matplotlib import pyplot as plt
import numpy as np
from fastf1 import plotting


#==== Functions ======================================
def individual_function(x):

    return -0.477811 * x**(4) + 2.26017 * x**(3) - 3.21407 * x**(2) + 0.51794 *x + 1.38617

def tyre_degrade_function(x):

    return -0.17482517 * x**(4) + 0.543900 * x**(3) - 0.41783216 * x**(2) - 0.141802 * x + 0.24055944

#==== Main ===========================================
if __name__ == "__main__":

    # Generate the x-Axis
    #laps = list(range(0, 100, 0.1))
    individual_values = list(np.arange(0, 2+0.05, 0.05))
    tyre_values = list(np.arange(0,1+0.05, 0.05))

    # Map the x-Axis to the function values
    individual_array = list(map(individual_function, individual_values))
    tyre_array = list(map(tyre_degrade_function, tyre_values))

    # Load the plot config
    #plotting.setup_mpl()

    # Plot the given array
    plt.plot(individual_values, individual_array, color="orangered")
    plt.xlabel("Individual Performance Parameter\nSum of Car Performance [0,1] and Driver Performance [0,1]", fontsize=15)
    plt.ylabel("Laptime Offset [s]", fontsize=15)
    plt.show()

    # Plot the given array
    plt.plot(tyre_values, tyre_array, color="green")
    plt.xlabel("Delta to Car in Front [Seconds]", fontsize=15)
    plt.ylabel("Additional Tyre Degradation [Laps]", fontsize=15)
    plt.show()

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

#==== Main ===========================================
if __name__ == "__main__":

    # Generate the x-Axis
    #laps = list(range(0, 100, 0.1))
    individual_values = list(np.arange(0, 2+0.05, 0.05))

    # Map the x-Axis to the function values
    individual_array = list(map(individual_function, individual_values))

    # Load the plot config
    #plotting.setup_mpl()

    # Plot the given array
    plt.plot(individual_values, individual_array, color="orangered")
    plt.xlabel("Individual Performance Parameter\nSum of Car Performance [0,1] and Driver Performance [0,1]")
    plt.ylabel("Laptime Offset [s]")
    plt.show()

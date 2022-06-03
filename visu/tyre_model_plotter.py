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
def soft_function(x):
    return round(x**(4) * 0.00043609 - x**(3) * 0.01003 + x**(2) * 0.08299 - x*0.36458 + 79.8878, 3)

def medium_function(x):
    return round(x**(4) * 1.58346733*10**(-5) - x**(3)*0.00094469 + x**(2)*0.0197911 - x*0.200544 + 79.92767, 3)

def hard_function(x):
    return round(x**(4) * 6.08866*10**(-6) - x**(3)*0.000321395 + x**(2)*0.005271977 - x*0.04700884 + 79.88238, 3)

#==== Main ===========================================
if __name__ == "__main__":

    # Generate the x-Axis
    laps = list(np.arange(0, 100+0.05, 0.05))

    # Map the x-Axis to the function values
    soft_array = list(map(soft_function, laps))
    medium_array = list(map(medium_function, laps))
    hard_array = list(map(hard_function, laps))


    # Plot the given array
    plt.plot(laps, soft_array, color="red", label="Soft")
    plt.plot(laps, medium_array, color="gold", label="Medium")
    plt.plot(laps, hard_array, color="grey", label="Hard")

    # Set the Axis Scales
    plt.xlim(0, 50)
    plt.ylim(77, 83)

    # Set the Axis Labels
    plt.xlabel("Tyre Life [Laps]")
    plt.ylabel("Laptime [s]")
    
    # Generate the Plot
    plt.legend()
    plt.show()

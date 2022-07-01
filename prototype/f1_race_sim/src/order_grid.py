"""
    Module to order the grid according to the race time
    and setting the fitting intervals betweent the cars

"""

#=====Functions=======================================
def order_grid(unsorted_grid):
    """
    Function to order the grid

    return - {list} - grid_sorted - List of Pointer to all car objects that are currently racing
    """ 

    # Order grid by race time at the end of the lap
    grid_sorted = sorted(unsorted_grid, key=lambda car: car.race_time)

    # Alter the positions according to race time
    for index in range(0, len(grid_sorted)):

        # Set the new position of this lap
        grid_sorted[index].position = index + 1

        # Compute the according intervals
        # But skip the driver on pos one
        if index == 0:
            grid_sorted[index].delta_to_car_infront = "-"
            continue

        grid_sorted[index].delta_to_car_infront = round(grid_sorted[index].race_time - grid_sorted[index - 1].race_time, 2)

    return grid_sorted
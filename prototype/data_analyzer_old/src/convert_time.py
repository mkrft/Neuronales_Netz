"""
    Convert the given times into numbers of seconds

"""

#=====Functions=======================================
def convert_time(time_str):
    """
    Convert the time string into according number of seconds
    
    param - {str} - time_str 

    return - {float} - seconds
    """

    string_split = time_str.split(":")
    return float(string_split[0]) * 60 + float(string_split[1])

"""
    F1 Race Simulator

    Test Module to start getting a hand on AI

    author:     Alexander Müller
    date:       03.11.2021
    version:    0.0.1

    Please contact us for further information via Git.

"""
#=====Libraries=======================================
import argparse

#=====Module Imports==================================
from src.ai_race_loop import ai_race_loop

#=====Program Entry===================================
if __name__ == "__main__":

    # Define args parser
    parser = argparse.ArgumentParser(description="Neural Network Parameters")
    parser.add_argument('--load_from_file', action='store_true', default=False, help='Load the weights from the file models/prediction_network_weigts')
    parser.add_argument('--log', action='store_true', default=False, help='Log the data of every single episode! So handle with care!')
    args = parser.parse_args()

    # Read input
    load_from_file = args.load_from_file
    log = args.log
    
    
    # Start the race!
    ai_race_loop(load=load_from_file, log=log)

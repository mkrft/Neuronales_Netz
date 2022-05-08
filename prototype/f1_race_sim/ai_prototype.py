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
    parser = argparse.ArgumentParser(description="Neural Network Parameters")
    parser.add_argument('--load_from_file', action='store_true', default=False,
    help='load the weights from the file src/prediction_network_weigts')
    args = parser.parse_args()
    load_from_file = args.load_from_file
    # Start the race!
    ai_race_loop(load_from_file)

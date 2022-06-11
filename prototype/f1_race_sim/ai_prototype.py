"""
    F1 Race Simulator

    Test Module to start getting a hand on AI

    author:     Alexander Müller
    date:       03.11.2021
    version:    1.0.0

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
    parser.add_argument('--selfplay', action='store_true', default=False, help='Instead of choosing a static action each race, take an older version of the ai as competitor - strategy (the same for every competitor!)')
    parser.add_argument('--test', action='store_true', default=False, help='Turn off the gradients and do not learn, just play the sim. Usefull for evaluating an already trained ai.')
    parser.add_argument('--mutate',action='store_true',default=False,help='Mutates weights if loaded from file')
    args = parser.parse_args()

    # Read input
    load_from_file = args.load_from_file
    log = args.log
    selfplay = args.selfplay
    test = args.test
    mutate = args.mutate
    
    
    # Start the race!
    ai_race_loop(load=load_from_file, log=log, selfplay=selfplay, test=test,mutate=mutate)

"""
    Definition of the neural network models to be used for creating the agents
"""

#=================== Libraries ====================
import torch 
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#=================== Code ====================
class DQNmodel(nn.Sequential):
    def __init__(self, inputlen : int, outputlen : int, load_weights_from_file : bool):
        super(DQNmodel, self).__init__()

        # activation function for each neuron
        self.nonlinearity = F.relu

        # layers
        # fixed : input is the length of the input data
        self.l1 = inputlen 
        # variable hidden layers
        self.l2 = 30
        self.l3 = self.l2
        # output is the number of actions to take
        self.l4 = outputlen

        # initialize the network layers
        self.f1 = nn.Linear(self.l1, self.l2)
        self.f2 = nn.Linear(self.l2, self.l3)
        self.f3 = nn.Linear(self.l3, self.l4)

        # TODO FIX PATHS AND ADD /models /logs
        if load_weights_from_file:
            self.load("./models/prediction_network_weights")



    def forward(self, x):
        # feed an input vector through the network
        x = self.nonlinearity(self.f1(x))
        x = self.nonlinearity(self.f2(x))
        x = self.f3(x)
        return x
    
    def load(self, filepath):
        self.load_state_dict(torch.load(filepath))


"""
    Definition of the neural network models to be used for creating the agents
"""

#=================== Libraries ====================
import torch 
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from src.mutate import mutate

#=================== Code ====================

class DQNmodel(nn.Sequential):
    def __init__(self, inputlen : int, outputlen : int, load_weights_from_file : bool, mutate:bool):
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
            # mutate if requested
            if mutate:
                self = mutate(self)


    def forward(self, x):
        # feed an input vector through the network
        x = self.nonlinearity(self.f1(x))
        x = self.nonlinearity(self.f2(x))
        x = self.f3(x)
        return x
    
    def load(self, filepath):
        self.load_state_dict(torch.load(filepath))


class DQNmodel_dueling(nn.Sequential):
    """
    Model for the dueling DQN algorithm : Separate evaluation of State and actions
    Doesn't work with mutation the same way the normal DQN does since we basicly have 3 Nets here
    """
    def __init__(self, inputlen : int, outputlen : int, load_weights_from_file : bool, mutate:bool):
        super(DQNmodel_dueling, self).__init__()

        # layers
        # fixed : input is the length of the input data
        self.l1 = inputlen 
        # variable hidden layers
        self.l2 = 30
        self.l3 = self.l2
        # output is the number of actions to take
        self.l4 = self.l2

        self.l_out = outputlen

        # Networks required for the the dueling DQN algorithm:
        # Value estimates the scalar value of a state, advantage that of all actions
        # Feature is the stuff that is equal for both, think of it as preprocessing the input

        self.feature_net = nn.Sequential(
                nn.Linear(self.l1, self.l2),
                nn.ReLU(),
                nn.Linear(self.l2, self.l3),
                nn.ReLU(),
        )

        self.value_net = nn.Sequential(
                nn.Linear(self.l3, self.l4),
                nn.ReLU(),
                nn.Linear(self.l4, 1)
        )

        self.advantage_net = nn.Sequential(
                nn.Linear(self.l3, self.l4),
                nn.ReLU(),
                nn.Linear(self.l4, self.l_out)
        )

        # TODO FIX PATHS AND ADD /models /logs
        if load_weights_from_file:
            self.load("./models/prediction_network_weights")
            # mutate if requested
            if mutate:
                self = mutate(self)

    def forward(self, x):
        # feed an input vector through the network
        features = self.feature_net(x)
        values = self.value_net.forward(features)
        advantages = self.advantage_net.forward(features)
        # Dueling DQN requires maximizing action to make q roughly equal Values, hence the - mean
        q_values = values + (advantages - torch.max(advantages))
        return q_values
    
    def load(self, filepath):
        self.load_state_dict(torch.load(filepath))



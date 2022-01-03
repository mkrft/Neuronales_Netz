import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()

        # Layers of the Network, take state as input and output values for the 4 actions
        self.fc1 = nn.Linear()
        self.fc2 = nn.Linear()

        self.activation = F.relu   # max(0, x) as nonlinearity

    def forward(self, x):
        x = torch.flatten(x)
        x = 

if __name__ == "__main__":


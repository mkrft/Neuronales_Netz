"""
    Model to build the agent from Keras to interact with
    our environment

"""
#=================== Libraries ====================
import numpy as np
import random
import torch 
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#=================== Code ====================

# A neural Network to predict pitstop rewards 
class Agent(nn.Module):
    def __init__(self, learning_rate, inputlen):
        super(Agent, self).__init__()
        self.reward = 0
        self.short_mem = np.array([])
        self.mem = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.lr = learning_rate

        # activation function for each neuron
        self.nonlinearity = F.relu

        # epsilon for policy
        self.epsilon = 1
        self.epsilon_decay = 0.001
        self.epsilon_min = 0.1

        # weight of later rewards
        self.gamma = 0.9

        # layer sizes, for now 3 layers
        # fixed : input is the length of the input data
        self.first = inputlen 
        # variable hidden layer
        self.second = 200
        # output is the number of actions to take
        self.third = 4

        # initialize the network layers
        self.f1 = nn.Linear(self.first, self.second)
        self.f2 = nn.Linear(self.second, self.third)

        # optimizer must be initiallized last because it needs all parameters (the weights)
        self.optimizer = optim.SGD(self.parameters(), lr=self.lr)

    def forward(self, x):
        # feed an input vector through the network
        x = self.nonlinearity(self.f1(x))
        x = self.nonlinearity(self.f2(x))
        x = F.softmax(x, dim=0)
        return x

    def add_replay(self, state, action, reward, next, done):
        # remember an action for replaying
        np.append(self.mem, [state, action, reward, next, done])

    def replay(self, mem, size):
        # replay some training examples
        if len(mem) > size:
            batch = random.sample(mem, size)
        else:
            batch = mem

        for state, action, reward, next, done in batch:
            self.train_single(state, action, reward, next, done)

    def decay_espilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon -= self.epsilon_decay


    def train_single(self, state, action, reward, next, done):
        # train on one example

        # tell pytorch that we are training the Network
        self.train()
        # since we are training we need the derivatives
        torch.set_grad_enabled(True)

        target = reward
        
        # convert state arrays to list of lists and then to tensors
        next_state = torch.tensor(next, dtype=torch.float32)
        state = torch.tensor(state, dtype=torch.float32 ,requires_grad=True)

        # approximately the value the network should give for current state + action
        if not done:
            target = reward + self.gamma * torch.max(self.forward(next_state)[0])

        # value for current state + all actions network gives
        out = self.forward(state)

        # make a target vector, needs to be the same shape as the network output
        target_vector = out.clone()
        target_vector[action] = target    # set the appropriate index
        target_vector.detach()      # dont need a gradient on this
        # print(f"target vector: {target_vector}")

        #optimize
        self.optimizer.zero_grad()
        loss = F.mse_loss(out, target_vector)
        loss.backward()
        self.optimizer.step()

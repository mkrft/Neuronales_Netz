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
    def __init__(self, learning_rate : float, inputlen : int):
        super(Agent, self).__init__()
        self.reward = 0
        self.short_mem = np.array([])
        self.mem = np.array([])
        self.lr = learning_rate
        # scores for logging the learning process
        self.scores = []

        # amount of episodes where the agent chooses purely random to explore strategies
        self.decay_gate = 0

        # activation function for each neuron
        self.nonlinearity = F.relu

        # epsilon for policy
        self.epsilon = 1
        self.epsilon_decay = 0.001
        self.epsilon_min = 0.0001

        # weight of later rewards
        self.gamma = 0.8

        # fixed : input is the length of the input data
        self.l1 = inputlen 
        # variable hidden layers
        self.l2 = 400
        # output is the number of actions to take
        self.l3 = 4

        # initialize the network layers
        self.f1 = nn.Linear(self.l1, self.l2)
        self.f2 = nn.Linear(self.l2, self.l3)

        # optimizer must be initiallized last because it needs all parameters (the weights)
        self.optimizer = optim.SGD(self.parameters(), lr=self.lr)

    def forward(self, x):
        # feed an input vector through the network
        x = self.nonlinearity(self.f1(x))
        x = self.f2(x)
        #x = F.softmax(x, dim=0)
        return x

    def add_replay(self, state, action, reward, next, done) -> None:
        # remember an action for replaying
        np.append(self.mem, [state, action, reward, next, done])

    def replay(self, size) -> None:
        # replay some training examples
        if len(self.mem) > size:
            batch = random.sample(self.mem, size)
        else:
            batch = self.mem

        for state, action, reward, next, done in batch:
            self.train_single(state, action, reward, next, done)

    def decay_epsilon(self, episode) -> None:
        if (self.epsilon > self.epsilon_min) and (episode > self.decay_gate):
            self.epsilon -= self.epsilon_decay
        elif episode > self.decay_gate:
            self.epsilon = self.epsilon_min


    def train_single(self, state, action, reward, next, done) -> None:
        # train on one example
        # TODO partially decouple the prediction and target networks

        # convert the input lists to tensors
        state = torch.tensor(state, dtype=torch.float32, requires_grad=True)
        next_state = torch.tensor(next, dtype=torch.float32, requires_grad=True)
        # tell pytorch that we are training the Network
        self.train()
        # since we are training we need the derivatives
        torch.set_grad_enabled(True)

        # approximately the value the network should give for current state + action
        if not done:
            predicted_next_action_rewards = self.forward(next_state)
            target = reward + self.gamma * torch.max(predicted_next_action_rewards)
        else:
            target = reward

        # value for previous state + all actions network gives
        out = self.forward(state)

        # make a target vector, needs to be the same shape as the network output
        target_vector = out.clone()
        # the target is what we computed before in out, but the action we took can be replaced with the calculated target value
        target_vector[action] = target
        target_vector.detach()      # dont need a gradient on this
        # print(f"target vector: {target_vector}")

        #optimize
        self.optimizer.zero_grad()
        loss = F.mse_loss(out, target_vector)
        loss.backward()
        self.optimizer.step()


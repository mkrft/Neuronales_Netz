"""
    Agent for making the pitstrat decisions and learning from examples.
    Implements a Double - DQN by wrapping around a simple neural net.

"""
#=================== Imports ======================
from src.dqn_model import DQNmodel

#=================== Libraries ====================
import numpy as np
import random
import copy
import torch 
import torch.nn.functional as F
import torch.optim as optim

#=================== Code ====================

# A neural Network to predict pitstop rewards 
class Agent():
    def __init__(self, learning_rate : float, inputlen : int, load : bool):
        # Network for predicting the Q - values
        self.prediction_dqn = DQNmodel(inputlen=inputlen, load_weights_from_file=load)
        # Network for prediction of the target vectors
        self.target_dqn = copy.deepcopy(self.prediction_dqn)

        # memory array for experience replay
        self.mem = np.array([])

        # scores for logging the learning process
        self.scores = []

        # optimizer for the prediction Network
        self.optimizer = optim.SGD(self.prediction_dqn.parameters(), lr=learning_rate)

        # amount of episodes where the agent chooses purely random to explore strategies
        self.decay_gate = 0

        # epsilon for policy
        self.epsilon_decay = 0.001
        self.epsilon_min = 0.0001
        if not load:
            self.epsilon = 1
        else:
            self.epsilon = self.epsilon_min
        # weight of later rewards
        self.gamma = 0.6

        # counter for copying the prediction network to the target net
        self.update_counter = 0

        # amount of updates it takes until the prediction is copied
        self.update_interval = 70


    def add_replay(self, state, action, reward, next, done) -> None:
        # remember an action for replaying
        np.append(self.mem, [state, action, reward, next, done])


    def forward(self, state):
        # pass a state to the prediction net and return the resulting output vector
        return self.prediction_dqn.forward(state)


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

        # convert the input lists to tensors
        state = torch.tensor(state, dtype=torch.float32, requires_grad=True)
        next_state = torch.tensor(next, dtype=torch.float32, requires_grad=True)
        # tell pytorch that we are training the Network
        self.prediction_dqn.train()
        # since we are training we need the derivatives
        torch.set_grad_enabled(True)

        # output of the prediction network
        out = self.prediction_dqn.forward(state)

        # output for the target network
        if not done:
            predicted_next_action_rewards = self.target_dqn.forward(next_state)
            target = reward + self.gamma * torch.max(predicted_next_action_rewards)
        else:
            target = reward

        # make a target vector, needs to be the same shape as the network output
        target_vector = out.clone()
        # the target is what we computed before in out, but the action we took can be replaced with the calculated target value
        target_vector[action] = target
        target_vector.detach()      # dont need a gradient on this
        # print(f"target vector: {target_vector}")

        # optimize
        self.optimizer.zero_grad()
        loss = F.mse_loss(out, target_vector)
        loss.backward()
        self.optimizer.step()

        self.update_counter += 1
        # copy the prediction net to the target net
        if (self.update_counter % self.update_interval) == 0:
            self.target_dqn.load_state_dict(self.prediction_dqn.state_dict())

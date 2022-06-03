"""
    Agent for making the pitstrat decisions and learning from examples.
    Implements a Double - DQN by wrapping around a simple neural net.

"""
#=================== Imports ======================
from src.dqn_model import DQNmodel
from src.config import MEMSIZE, EXPLORATION_TIME, RACE_DISTANCE

#=================== Libraries ====================
import numpy as np
import random
import math
import copy
import torch 
import torch.nn.functional as F
import torch.optim as optim
from collections import deque

#=================== Helpers =================

def get_epsilon_decay_exponential(target_episodes, min_val):
    """
    get the epsilon value for exponential decay.
    converges to min_val after target_episodes.
    Alternative to the linear approach.
    """
    return math.exp(math.log(min_val)/target_episodes)

#=================== Code ====================

# A neural Network to predict pitstop rewards 
class Agent():
    def __init__(self, learning_rate : float, inputlen : int, outputlen : int, load : bool, mutate:bool):
        # Network for predicting the Q - values
        self.prediction_dqn = DQNmodel(inputlen=inputlen,outputlen=outputlen,load_weights_from_file=load,mutate=mutate)
        # Network for prediction of the target vectors
        self.target_dqn = copy.deepcopy(self.prediction_dqn)

        # memory array for experience replay
        self.mem = deque(maxlen=MEMSIZE)

        # scores for logging the learning process
        self.scores = []
        self.losses = []

        # optimizer for the prediction Network
        self.optimizer = optim.SGD(self.prediction_dqn.parameters(), lr=learning_rate)

        # amount of episodes where the agent chooses purely random to explore strategies
        self.decay_gate = 0

        # epsilon for policy
        self.epsilon_decay = 1/EXPLORATION_TIME

        self.epsilon_min = 0.005
        if not load:
            self.epsilon = 1
        else:
            self.epsilon = self.epsilon_min

        # weight of later rewards
        self.gamma = 0.999

        # counter for copying the prediction network to the target net
        self.update_counter = 0

        # amount of updates it takes until the prediction is copied
        self.update_interval = 30 * RACE_DISTANCE


    def add_replay(self, state, action, reward, next, done) -> None:
        # remember an action for replaying
        self.mem.append((state, action, reward, next, done))


    def forward(self, state):
        # pass a state to the prediction net and return the resulting output vector
        return self.prediction_dqn.forward(state)


    def replay(self, size) -> None:
        # replay some training examples one by one
        if len(self.mem) > size:
            batch = random.sample(self.mem, size)
        else:
            return

        for state, action, reward, next, done in batch:
            self.train_single(state, action, reward, next, done)


    def decay_epsilon_linear(self, episode) -> None:
        if (self.epsilon > self.epsilon_min) and (episode > self.decay_gate):
            self.epsilon -= self.epsilon_decay
        elif episode > self.decay_gate:
            self.epsilon = self.epsilon_min


    def decay_epsilon_exponential(self, episode) -> None:
        if (self.epsilon > self.epsilon_min) and (episode > self.decay_gate):
            self.epsilon *= self.epsilon_decay
        elif episode > self.decay_gate:
            self.epsilon = self.epsilon_min


    def train_single(self, state, action, reward, next, done) -> None:
        # train on one example

        # convert the input lists to tensors
        # tell pytorch that we are training the Network
        self.prediction_dqn.train()
        # since we are training we need the derivatives
        torch.set_grad_enabled(True)

        # output of the prediction network
        out = self.prediction_dqn.forward(state)

        # output for the target network
        if not done:
            predicted_next_action_rewards = self.target_dqn.forward(next)
            target = reward + self.gamma * torch.max(predicted_next_action_rewards)
        else:
            target = reward

        # make a target vector, needs to be the same shape as the network output
        target_vector = out.clone()
        # the target is what we computed before in out, but the action we took can be replaced with the calculated target value
        target_vector[action] = target
        target_vector.detach()      # dont need a gradient on this

        # optimize
        self.optimizer.zero_grad()
        loss = F.mse_loss(out, target_vector)
        self.losses.append(loss.item())
        loss.backward()

        self.optimizer.step()

        self.update_counter += 1
        # copy the prediction net to the target net
        if (self.update_counter % self.update_interval) == 0:
            self.target_dqn.load_state_dict(self.prediction_dqn.state_dict())


    def train_batch(self, size) -> None:
        """
        Train on a whole batch of experiences at once using the DDQN algorithm for additional
        separation of the prediction and Target networks
        """
        if len(self.mem) < 1000:
            return

        batch = random.sample(self.mem, size)
        # reorganize the data by separating it 
        states, actions, rewards, nexts, dones = map(torch.stack, zip(*batch))

        self.prediction_dqn.train()
        # since we are training we need the derivatives
        torch.set_grad_enabled(True)

        # outputs of the prediction network
        # indexing: all elements and the action as index is what this means
        outs = self.prediction_dqn.forward(states)[np.arange(0, size), actions]

        # ask the prediction network for the best action to take
        predicted_best_actions = torch.argmax(self.prediction_dqn.forward(nexts), axis=1)
        predicted_next_action_rewards = self.target_dqn(nexts)[np.arange(0, size), predicted_best_actions]

        # calculation for the standard DQN - algorithm
        #predicted_next_action_rewards = self.target_dqn.forward(nexts)

        # all target values, important to set next to 0 if done
        # calculation for Standard DQN
        #targets = rewards + (self.gamma * torch.max(predicted_next_action_rewards, axis=1).values) * (1-dones.float())
        # calculation for DDQN
        targets = rewards + (self.gamma * predicted_next_action_rewards) * (1-dones.float())


        # optimize
        loss = F.mse_loss(outs, targets)
        self.optimizer.zero_grad()
        self.losses.append(loss.item())
        loss.backward()

        # limit size of gradient since that can explode with big errors
        for param in self.prediction_dqn.parameters():
            param.grad.data.clamp(-100, 100)

        self.optimizer.step()

        self.update_counter += 1
        # copy the prediction net to the target net
        if (self.update_counter % self.update_interval) == 0:
            self.target_dqn.load_state_dict(self.prediction_dqn.state_dict())

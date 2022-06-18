"""
    Agent for making the pitstrat decisions and learning from examples.
    Implements a Double - DQN by wrapping around a simple neural net.

"""
#=================== Imports ======================
from src.dqn_model import DQNmodel, DQNmodel_dueling
from src.build_grid import build_grid
from src.ai_race_loop_helpers import determine_ai_action, get_state, get_reset_state
from src.race_step import step
from src.actions import Actions
from src.config import MEMSIZE, EXPLORATION_TIME, RACE_DISTANCE

#=================== Libraries ====================
import numpy as np
import random
import math
import copy
import time
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
        self.optimizer = optim.Adam(self.prediction_dqn.parameters(), lr=learning_rate)

        # Boltzmann - policy parameters
        self.temperature_initial = 1.0
        self.temperature_min = 0.1
        self.temperature_decay = (self.temperature_initial - self.temperature_min) / EXPLORATION_TIME
        self.temperature = self.temperature_initial

        # Epsilon - policy parameters
        self.epsilon_min = 0.01

        if not load:
            self.epsilon = 1
        else:
            self.epsilon = 0

        # amount of episodes where the agent chooses purely random to explore strategies
        self.decay_gate = 0

        # epsilon for policy
        self.epsilon_decay = (self.epsilon - self.epsilon_min)/EXPLORATION_TIME

        # weight of later rewards
        self.gamma = 0.99

        # counter for copying the prediction network to the target net
        self.update_counter = 0

        # amount of updates it takes until the prediction-network is copied to the target-network
        self.update_interval = 750


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

    def decay_temperature(self):
        self.temperature -= self.temperature_decay

    def decay_epsilon_exponential(self, episode) -> None:
        if (self.epsilon > self.epsilon_min) and (episode > self.decay_gate):
            self.epsilon *= self.epsilon_decay
        elif episode > self.decay_gate:
            self.epsilon = self.epsilon_min


    def train_single(self, state, action, reward, next, done) -> None:
        """
        Train the network on one example from the replay memory
        """

        # convert the input lists to tensors
        # tell pytorch that we are training the Network
        self.prediction_dqn.train()
        # since we are training we need the derivatives
        torch.set_grad_enabled(True)

        # output of the prediction network
        out = self.prediction_dqn.forward(state)

        # output for the target network
        if not done:
            best_predicted_action = torch.argmax(self.prediction_dqn.forward(next))
            predicted_next_action_reward = self.target_dqn.forward(next)[best_predicted_action]
            target = reward + self.gamma * predicted_next_action_reward
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
        torch.nn.utils.clip_grad_norm_(self.prediction_dqn.parameters(), 1000000)

        self.optimizer.step()

        self.update_counter += 1
        # copy the prediction net to the target net
        if (self.update_counter % self.update_interval) == 0:
            self.target_dqn.load_state_dict(self.prediction_dqn.state_dict())


    def randomly_fill_memory(self):
        """
        fill the initial memory size with transitions generated by a random policy
        """
        for episode in range(0, round(MEMSIZE / RACE_DISTANCE)):
            lap = 0
            done = False
            log = False
            grid = build_grid()
            startindex = 0
            #startindex = random.randrange(0, len(grid))
            ai_car = grid[startindex]

            actions = {}
            state = get_reset_state()

            # completely random action for the AI - car
            actions[ai_car] = Actions(random.randint(0, len(Actions)-1))
            while lap < RACE_DISTANCE:
                grid, lap, rewards = step(grid, actions, lap, log)

                if lap == RACE_DISTANCE:
                    done = True

                n_state = get_state(ai_car, lap)
                self.add_replay(state, torch.tensor(actions[ai_car].value), torch.tensor(rewards[ai_car]), n_state, torch.tensor(done), episode)
                actions.clear()

                for car in grid:
                    if car == ai_car:
                        actions[car] = Actions(random.randint(0, len(Actions)-1))
                    elif lap == 15:
                        actions[car] = Actions.MEDIUM
                    elif lap == 48:
                        actions[car] = Actions.MEDIUM
                state = n_state



    def train_batch(self, size) -> None:
        """
        Train on a whole batch of experiences at once using the DDQN algorithm for additional
        separation of the prediction and Target networks.
        This means one gradient step is taken from sampling the whole Batch.
        """

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

        # all target values, important to set next to 0 if done
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

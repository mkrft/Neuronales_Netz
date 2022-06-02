from src.dqn_model import DQNmodel
import numpy as np


def mutate(model:DQNmodel):
    allparams = model.parameters()
    for param in allparams:
        print(param)

'''
Module to hold the functions that are used to mutate given parameters of 
a dqn model
'''
#=====Imports=========================================

#=====Module Imports==================================

#=====Libraries=======================================
import numpy as np
import torch

#=====Functions=======================================
#Based on https://stackoverflow.com/questions/63951120/how-to-mutate-weights-of-a-nn-in-pytorch
def mutate(model):
    '''
    Function that mutates a given model

    param - {DQNmodel} - model - neural network model that needs to be mutated

    return - {DQNmodel} - model - mutated network model

    '''

    #TODO Debug, I'm not sure wheter the model is mutated, due to callbyreference and callbyvalue thinks -> don't tested because lazyness
    for name, param in model.named_parameters():
        if str(name).__contains__("weight"):
            param.data += _mutate_weight(param)
        else:
            param.data += _mutate_bias(param)

    return model

        
#TODO Necessary to mutate biases? If so, use a function that causes an effect
def _mutate_bias(param):
    '''
    Function that calculates a mutation tensor for a given bias input object
    Current zero tensor don't causes any effect

    param - {obj} - param - dqnmodel bias parameter that needs to be mutated

    return - {tensor} - mutation - tensor that holds the mutation of the biases
    '''
    mutation = torch.zeros(param.size())
    return mutation

#Based on https://stackoverflow.com/questions/63951120/how-to-mutate-weights-of-a-nn-in-pytorch
#TODO Think of another function that takes out current weights into consideration, to prevent unscaled mutation of weight
def _mutate_weight(param):
    '''
    Function that calculates a mutation tensor for a given weight input object
    Current tensor causes a random mutation

    param - {obj} - param - dqnmodel weight parameter that needs to be mutated

    return - {tensor} - mutation - tensor hat holds the mutation of the biases
    
    '''
    mutation_power = 0.4
    #mutation = mutation_power * torch.rand_like(param)
    mutation = mutation_power * torch.randn(param.size())
    return mutation
"""
    Model to build the agent from Keras to interact with
    our environment

"""

#=====Libraries=======================================
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

#=====Functions=======================================
def build_agent(model, actions):
    """
    Build our RL Agent
    """
    
    agent = DQNAgent(
        model=model,
        memory=SequentialMemory(limit=50000, window_length=1),
        policy=BoltzmannQPolicy(),
        nb_actions=actions,
        nb_steps_warmup=10,
        target_model_update=1e-2
    )

    return agent
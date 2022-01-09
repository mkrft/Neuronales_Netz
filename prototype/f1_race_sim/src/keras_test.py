"""
    Testing the KERAS Library to optimize our
    F1 Strategy AI by looking into the 

"""

#=====Libraries=======================================
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

#=====Functions=======================================
def build_model(states, actions):
    """
    Buidler for our Keras Model to train with
    """

    model = Sequential()
    model.add(Dense(24, activation="relu", input_shape=states))
    model.add(Dense(24, activation="relu"))
    model.add(Dense(actions, activation="linear"))

    return model
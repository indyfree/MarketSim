#!/usr/bin/env python

import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

# from rl.policy import BoltzmannQPolicy
from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory

import marketsim


def main():
    ENV_NAME = "MarketSim-v0"
    env = gym.make(ENV_NAME)
    np.random.seed(123)
    env.seed(123)
    nb_actions = env.action_space.n

    # Next, we build a very simple model.
    model = Sequential()
    model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
    model.add(Dense(16))
    model.add(Activation("relu"))
    model.add(Dense(16))
    model.add(Activation("relu"))
    model.add(Dense(16))
    model.add(Activation("relu"))
    model.add(Dense(nb_actions))
    model.add(Activation("linear"))
    print(model.summary())

    # Finally, we configure and compile our agent. You can use every
    # built-in Keras optimizer and even the metrics!
    memory = SequentialMemory(limit=50000, window_length=1)
    # policy = BoltzmannQPolicy()
    policy = LinearAnnealedPolicy(
        EpsGreedyQPolicy(),
        attr="eps",
        value_max=1.0,
        value_min=0.1,
        value_test=0.05,
        nb_steps=40000,
    )
    dqn = DQNAgent(
        model=model,
        nb_actions=nb_actions,
        memory=memory,
        nb_steps_warmup=1000,
        target_model_update=1e-2,
        policy=policy,
    )
    dqn.compile(Adam(lr=1e-3), metrics=["mae"])

    # Okay, now it's time to learn something! We visualize the training
    # here for show, but this # slows down training quite a lot. You can
    # always safely abort the training prematurely using Ctrl + C.
    dqn.fit(env, nb_steps=50000, visualize=False, log_interval=2000, verbose=1)

    # After training is done, we save the final weights.
    dqn.save_weights("dqn_{}_weights.h5f".format(ENV_NAME), overwrite=True)

    # Finally, evaluate our algorithm for 5 episodes.
    dqn.test(env, nb_episodes=5, visualize=False)


if __name__ == "__main__":
    main()

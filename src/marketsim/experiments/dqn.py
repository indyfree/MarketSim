#!/usr/bin/env python

import numpy as np
import gym

import marketsim  # noqa: F401
from marketsim import agents


def main():
    ENV_NAME = "MarketSim-v0"
    env = gym.make(ENV_NAME)
    np.random.seed(123)
    env.seed(123)

    # Create Simple DQN Agent
    dqn = agents.SimpleDQN(env.observation_space.shape, env.action_space.n, 50000)

    # Okay, now it's time to learn something! You can
    # always safely abort the training prematurely using Ctrl + C.
    dqn.train(env, steps=500000)

    # Evaluate our algorithm for 5 episodes.
    dqn.test(env, episodes=5)


if __name__ == "__main__":
    main()

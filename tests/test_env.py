#!/usr/bin/env python

# core modules
import math
import unittest

# 3rd party modules
import gym

# internal modules
import marketsim


class Environments(unittest.TestCase):
    def test_env(self):
        env = gym.make("MarketSim-v0")
        env.seed(123)
        env.observation_space.sample()
        env.action_space.sample()
        env.reset()
        env.step(0)

    def test_random_agent(self):
        env = gym.make("MarketSim-v0")
        env.seed(123)
        ob = env.reset()
        print("Init: {} steps left".format(ob[0]))

        cum_reward = 0
        for i in range(10):
            print("--- Timestep: {} ----".format(i))
            a = env.action_space.sample()
            ob, reward, done, _ = env.step(a)
            cum_reward += reward
            print("Reward: {:.2f} EUR".format(reward))
            print("Observation: {} steps left".format(ob[0]))
            if done:
                ob = env.reset()
                print("Reset: {} steps left".format(ob[0]))

        print("Mean reward {:.2f} EUR".format(cum_reward / 5))
        print("Total reward {:.2f} EUR".format(cum_reward))


if __name__ == "__main__":
    unittest.main()

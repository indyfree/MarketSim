#!/usr/bin/env python

# core modules
import unittest

# 3rd party modules
import gym

# internal modules
import marketsim  # noqa: F401


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
        print("Init: {} steps left".format(ob))

        cum_reward = 0
        for i in range(10):
            print("--- Timestep: {} ----".format(i))
            a = env.action_space.sample()
            print("Action: No: {}".format(a))
            ob, reward, done, _ = env.step(a)
            cum_reward += reward
            print("Reward: {:.2f} EUR".format(reward))
            print("Observation: {} steps left".format(ob))
            if done:
                ob = env.reset()
                print("Reset: {} steps left".format(ob))

        print("Mean reward {:.2f} EUR".format(cum_reward / 10))
        print("Total reward {:.2f} EUR".format(cum_reward))


if __name__ == "__main__":
    unittest.main()

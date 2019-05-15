#!/usr/bin/env python

# core modules
import random

# 3rd party modules
from gym import spaces
import gym
import numpy as np

# internal modules
from marketsim import simulation


class MarketEnv(gym.Env):
    """
    Define a simple market environment.

    The environment defines which actions can be taken at which point and
    when the agent receives which reward.
    """

    def __init__(self):
        # General variables defining the environment
        self.MAX_PRICE = 2.0
        self.MAX_TIME_STEPS = 4
        self.PRODUCT_PRICE = 0.5

        # Create Simulation with environment parameters
        self.market = simulation.IntradayMarket(
            product_price=self.PRODUCT_PRICE, lead_time=self.MAX_TIME_STEPS
        )

        # Environment state variables
        self.curr_step = 0
        self.done = False

        # Define what the agent can do
        # Sell at 0.00 EUR, 0.10 Euro, ..., 2.00 Euro
        self.action_space = spaces.Discrete(21)

        # Observation is the remaining time
        self.observation_space = spaces.Discrete(self.MAX_TIME_STEPS + 1)

    def step(self, action):
        """
        The agent takes a step in the environment.

        Parameters
        ----------
        action : int

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        if self.done:
            raise RuntimeError("Episode is done")

        self.curr_step += 1

        reward = self._take_action(action)
        ob = self._get_state()

        return ob, reward, self.done, {}

    def _take_action(self, action):
        # Determine price from action
        price = (float(self.MAX_PRICE) / (self.action_space.n - 1)) * action

        # Interact with simulation
        reward, sold = self.market.trade_offer(price)

        # When is episode done?
        if sold or self.market.remaining_slots == 0:
            self.done = True

        return reward

    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.

        Returns
        -------
        observation (object): the initial observation of the space.
        """
        self.curr_step = 0
        self.done = False
        self.market.new_product()
        return self._get_state()

    def _get_state(self):
        """Get the observation."""
        ob = self.MAX_TIME_STEPS - self.curr_step
        return ob

    def seed(self, seed):
        random.seed(seed)
        np.random.seed(seed)

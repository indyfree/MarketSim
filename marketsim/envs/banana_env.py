#!/usr/bin/env python

# core modules
import logging.config
import pkg_resources
import random

# 3rd party modules
from gym import spaces
import cfg_load
import gym
import numpy as np

# internal modules
from gym_banana import simulation

# Set up logger
path = "logger_config.yaml"  # always use slash in packages
filepath = pkg_resources.resource_filename("gym_banana", path)
config = cfg_load.load(filepath)
logging.config.dictConfig(config["LOGGING"])


class BananaEnv(gym.Env):
    """
    Define a simple Banana environment.

    The environment defines which actions can be taken at which point and
    when the agent receives which reward.
    """

    def __init__(self):
        self.__version__ = "0.1.0"
        logging.info("BananaEnv - Version {}".format(self.__version__))

        # General variables defining the environment
        self.MAX_PRICE = 2.0
        self.TOTAL_TIME_STEPS = 4

        # Simulation
        self.market = simulation.IntradayMarket(self.TOTAL_TIME_STEPS)

        # Environment state variables
        self.curr_step = 0
        self.done = False

        # Define what the agent can do
        # Sell at 0.00 EUR, 0.10 Euro, ..., 2.00 Euro
        self.action_space = spaces.Discrete(21)

        # Observation is the remaining time
        low = np.array([0.0])  # remaining_tries
        high = np.array([self.TOTAL_TIME_STEPS])  # remaining_tries
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

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
        # TODO: Determine price from action
        price = (float(self.MAX_PRICE) / (self.action_space.n - 1)) * action

        # print("Action: bid {:.2f} EUR".format(price))
        # TODO: Interact with simulation
        reward, sold = self.market.trade_offer(price)

        # TODO: When is done?
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

    def _render(self, mode="human", close=False):
        return

    def _get_state(self):
        """Get the observation."""
        ob = [self.TOTAL_TIME_STEPS - self.curr_step]
        return ob

    def seed(self, seed):
        random.seed(seed)
        np.random.seed(seed)

# flake8: noqa
import marketsim.agents
import marketsim.simulation

from gym.envs.registration import register

register(id="MarketSim-v0", entry_point="marketsim.envs:MarketEnv")

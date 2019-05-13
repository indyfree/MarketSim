import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(id="MarketSim-v0", entry_point="gym_banana.envs:BananaEnv")

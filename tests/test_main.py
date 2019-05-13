#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest

# 3rd party modules
import gym

# internal modules
import gym_banana
from gym_banana import simulation
from gym_banana.simulation.market import selling_chance


class Environments(unittest.TestCase):

    def test_probability(self):
        price = 0
        self.assertTrue(1 == selling_chance(price))

        price = 1
        self.assertTrue(0.5 > selling_chance(price))

        price = math.inf
        self.assertTrue(0 == selling_chance(price))

    def test_sim(self):
        market = simulation.IntradayMarket(slots_ahead=2, max_price=2)

        reward = market.trade_offer(0)
        self.assertTrue(0 == reward)

        self.assertRaises(RuntimeError, market.trade_offer, 0)

        market.reset()
        reward = market.trade_offer(0)
        self.assertTrue(0 == reward)

        market.reset()
        reward = market.trade_offer(math.inf)
        self.assertTrue(0 == reward)

        reward = market.trade_offer(math.inf)
        self.assertTrue(0 == reward)

        self.assertRaises(RuntimeError, market.trade_offer, math.inf)


if __name__ == "__main__":
    unittest.main()

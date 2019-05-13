#!/usr/bin/env python

# core modules
import math
import unittest

# internal modules
from marketsim.simulation import AlreadySoldError, LeadtimePassedError, IntradayMarket


class Environments(unittest.TestCase):
    def test_probability(self):
        market = IntradayMarket()

        price = 0
        self.assertTrue(1 == market.selling_chance(price))

        price = 1
        self.assertTrue(0.5 > market.selling_chance(price))

        price = math.inf
        self.assertTrue(0 == market.selling_chance(price))

    def test_sim(self):
        market = IntradayMarket(lead_time=1)

        # 1. Succesfully sell
        reward, sold = market.trade_offer(0)
        self.assertTrue(0 == reward)
        self.assertTrue(sold)

        # 2. Already sold
        market.new_product(lead_time=1)
        reward, sold = market.trade_offer(0)
        self.assertTrue(sold)
        self.assertRaises(AlreadySoldError, market.trade_offer, 0)
        self.assertTrue(0 == reward)

        # 3. Not sold in time
        market.new_product(lead_time=2)
        reward, sold = market.trade_offer(math.inf)
        self.assertFalse(sold)
        self.assertTrue(0 == reward)
        reward, sold = market.trade_offer(math.inf)
        self.assertFalse(sold)
        self.assertTrue(0 == reward)
        self.assertRaises(LeadtimePassedError, market.trade_offer, math.inf)


if __name__ == "__main__":
    unittest.main()

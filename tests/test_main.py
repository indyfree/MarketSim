#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest

# 3rd party modules
import gym

# internal modules
import gym_banana


class Environments(unittest.TestCase):

    def test_probability(self):
        price = 0
        self.assertTrue(1 == selling_chance(price))

        price = 1
        self.assertTrue(0.5 > selling_chance(price))

        price = math.inf
        self.assertTrue(0 == selling_chance(price))


if __name__ == "__main__":
    unittest.main()

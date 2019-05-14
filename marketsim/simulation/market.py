#!/usr/bin/env python

import math
import random


class IntradayMarket:
    """
    Simulation of a simplified Intraday Continuous Market trading process.

    Taking the role of an electricity generator that wants to sell an
    electricity product within a given lead time in discrete time slots.
    """

    def __init__(self, product_price=1, lead_time=1):
        self.default_lead_time = lead_time
        self.default_product_price = product_price

        self.new_product(product_price, lead_time)

    def new_product(self, product_price=None, lead_time=None):
        """
        Create new electricity product with a given lead time
        that we aim to place on the market

        Parameters
        ----------
        lead_time: int

        """
        self.is_sold = False

        if not lead_time:
            lead_time = self.default_lead_time

        if not product_price:
            product_price = self.default_product_price

        self.remaining_slots = lead_time
        self.product_price = product_price

    def trade_offer(self, price):
        """
        Places a trade offer on the market

        Parameters
        ----------
        price: float

        Returns
        ------
        profit, is_sold : tuple

        profit (float):
               - 0 if product not sold in current slot.
               - [price] - [product_price] in EUR if the product is sold.
               - [product_price] in EUR if lead time passed.
        """
        if self.is_sold:
            raise AlreadySoldError("Electricity product already sold")

        if self.remaining_slots <= 0:
            raise LeadtimePassedError("Lead time passed")

        succesful_trade = random.random() < self.selling_chance(price)
        self.remaining_slots -= 1

        if succesful_trade:
            profit = price - self.product_price
            self.is_sold = True
        elif self.remaining_slots == 0:
            profit = -self.product_price
        else:
            profit = 0

        return (profit, self.is_sold)

    def selling_chance(self, x):
        """Probability that the product will be sold at price x."""
        return math.exp(-x)


class AlreadySoldError(RuntimeError):
    def __init__(self, message):
        self.message = message


class LeadtimePassedError(RuntimeError):
    def __init__(self, message):
        self.message = message

#!/usr/bin/env python

import math
import random


class IntradayMarket:
    """
    Simulation of a simplified Intraday Continuous Market trading process.

    Taking the role of an electricity generator that wants to sell an
    electricity product within a given lead time in discrete time slots.
    """

    def __init__(self, lead_time=1):
        self.default_lead_time = lead_time
        self.new_product(lead_time)

    def new_product(self, lead_time=None):
        """
        Create new electricity product with a given lead time
        that we aim to place on the market

        Parameters
        ----------
        lead_time: int

        """
        self.is_sold = False

        if lead_time is None:
            lead_time = self.default_lead_time

        self.remaining_slots = lead_time

    def trade_offer(self, price):
        """
        Places a trade offer on the market

        Parameters
        ----------
        price: float

        Returns
        ------
        offer_return, is_sold : tuple

        offer_return (float):
            Return of the offer is 0 EUR if product not sold,
            and [price] in EUR if the product is sold.
        """
        if self.is_sold:
            raise AlreadySoldError("Electricity product already sold")

        if self.remaining_slots <= 0:
            raise LeadtimePassedError("Lead time passed")

        succesful_trade = random.random() < self.selling_chance(price)
        self.remaining_slots -= 1

        if succesful_trade:
            offer_return = price
            self.is_sold = True
        else:
            offer_return = 0

        return (offer_return, self.is_sold)

    def selling_chance(self, x):
        """Probability that a banana will be sold at price x."""
        return math.exp(-x)


class AlreadySoldError(RuntimeError):
    def __init__(self, message):
        self.message = message


class LeadtimePassedError(RuntimeError):
    def __init__(self, message):
        self.message = message

# MarketSim

This repository contains a PIP package which is an OpenAI environment for
simulating an enironment in which electricity products get sold.

## Installation

Install the [OpenAI gym](https://gym.openai.com/docs/).

Then install this package via

```
pip install -e .
```

## Usage

```
import gym
import marketsim

env = gym.make('MarketSim-v0')
```

See https://github.com/matthiasplappert/keras-rl/tree/master/examples for some
examples.


## The Environment

Imagine an electricity generator that sells electricity on the Intraday
Continous Market shortly before delivery, for example one hour, thats
4 timeslots of 15-minutes. The generator places trade-offers on the market and
can update the offered price every timeslot before delivery.
The probability buyers will buy the electricity product is given by
$$p(x) = e^(-x))$$
where x is the offered price by the generator. If the generator can not sell the
electricity before delivery, the reward is the negative generation costs _z_. If
the generator succesfully sells the electricity the reward is x - z.

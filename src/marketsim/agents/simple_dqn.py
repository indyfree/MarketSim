#!/usr/bin/env python

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

# from rl.policy import BoltzmannQPolicy
from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory


class SimpleDQN:
    def __init__(self, observation_shape, nb_actions, eps_steps):
        # First, we build a very simple NN model.
        model = Sequential()
        model.add(Flatten(input_shape=(1,) + observation_shape))
        model.add(Dense(16))
        model.add(Activation("relu"))
        model.add(Dense(16))
        model.add(Activation("relu"))
        model.add(Dense(16))
        model.add(Activation("relu"))
        model.add(Dense(nb_actions))
        model.add(Activation("linear"))
        print(model.summary())

        # Next, we configure and compile our agent. You can use every
        # built-in Keras optimizer and even the metrics!
        memory = SequentialMemory(limit=50000, window_length=1)

        # policy = BoltzmannQPolicy()
        policy = LinearAnnealedPolicy(
            EpsGreedyQPolicy(),
            attr="eps",
            value_max=1.0,
            value_min=0.1,
            value_test=0.05,
            nb_steps=eps_steps,
        )
        self.dqn = DQNAgent(
            model=model,
            nb_actions=nb_actions,
            memory=memory,
            nb_steps_warmup=1000,
            target_model_update=1e-2,
            policy=policy,
        )

        self.dqn.compile(Adam(lr=1e-3), metrics=["mae"])

    def train(self, env, steps):
        self.dqn.fit(env, nb_steps=steps, visualize=False, log_interval=2000, verbose=1)

        # After training is done, we save the final weights.
        self.dqn.save_weights("dqn_weights.h5f", overwrite=True)

    def test(self, env, episodes):
        # Finally, evaluate our algorithm for 5 episodes.
        self.dqn.test(env, nb_episodes=episodes, visualize=False)

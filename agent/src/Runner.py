import tensorflow as tf
import numpy as np
import math
import random

class Runner:
    def __init__(self, sess, env, model, memory, max_eps, min_eps, decay):
        self._sess = sess
        self._env = env
        self._model = model
        self._memory = memory
        self._max_eps = max_eps
        self._min_eps = min_eps
        self._eps = max_eps
        self._decay = decay
        self._reward_store = []
        self._steps = 0

    def run(self):
        state = self._env.reset()
        tot_reward = 0

        while True:
            action = self.choose_action(state)
            next_state, reward, done = self._env.step(action)

            # reward modifier?

            if done is True:
                next_state = None

            self._memory.add_sample((state, reward, action, next_state))
            # self.replay()

            self._steps += 1
            self._eps = self._min_eps + (self._max_eps) * (self._decay)

            state = next_state
            tot_reward += reward

            print(done)
            if done is True:
                self._reward_store.append(tot_reward)
                break
        print("Episode reward: {}".format(tot_reward))

    def choose_action(self, state):
        if random.random() < 1:
            return self._env.sample_random_action()
        else:
            return self._model.predict_one(np.array(tuple(state)), self._sess)

    def replay(self):
        batch = self._memory.sample(self._model._batch_size)
        states = np.array([val[0] for val in batch])
        next_states = np.array([np.zeros(self._model._num_states) if val[3] is None else tuple(val[3]) for val in batch])
        # predict qsa given a batch of states
        q_s_a = self._model.predict_batch(states, self._sess)
        # predict prime(qsa)
        q_s_a_d = self._model.predict_batch(next_states, self._sess)
        # training arrays
        x = np.zeros((len(batch), self._model._num_states))
        y = np.zeros((len(batch), self._model._num_actions))
        for i, b in enumerate(batch):
            state, action, reward, next_state = b[0], b[1], b[2], b[3]

            # Structure the training data

            x[i] = None #?
            y[i] = None #?

        self._model.train_batch(self._sess, x, y)
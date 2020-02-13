import tensorflow as tf
import numpy as np
import math
import random
import time

class Runner:
    def __init__(self, sess, env, model, memory, max_eps, min_eps, decay, timestep=0):
        self._sess = sess
        self._env = env
        self._model = model
        self._memory = memory
        self._max_eps = max_eps
        self._min_eps = min_eps
        self._eps = max_eps
        self._decay = decay
        self._reward_store = []
        self._ending_vec_store = []
        self._steps = 0
        self._timestep = timestep

    def run(self):
        state, _, _ = self._env.reset()
        tot_reward = 0

        while True:
            time.sleep(self._timestep)
            action = self.choose_action(state)
            action_int = int(np.argmax(action))
            next_state, reward, done = self._env.step(action_int)

            # reward modifier?

            if done is True:
                next_state = None

            self._memory.add_sample((state, reward, action, next_state))
            self.replay()

            self._steps += 1
            self._eps = self._min_eps + (self._eps * self._decay)

            state = next_state
            tot_reward += reward

            if done is True or self._steps > 20000:
                self._reward_store.append(tot_reward)
                self._ending_vec_store.append(self._env.env.position_vec_prev)
                break

    def choose_action(self, state):
        if random.random() < self._eps:
            return self._env.sample_random_action()
        else:
            return self._model.predict_one(np.array(tuple(state)), self._sess).reshape([self._model._num_actions])

    def replay(self):
        GAMMA = 0.95
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
            state, reward, action, next_state = b[0], b[1], b[2], b[3]

            # Structure the training data
            # TODO: Maximize / minimize reward of one-hot action

            current_q = q_s_a[i]

            if next_state is None:
                current_q[int(np.argmax(action))] = reward
            else:
                current_q[int(np.argmax(action))] = reward * GAMMA * np.amax(q_s_a_d)

            x[i] = state #?
            y[i] = current_q #?

        self._model.train_model(self._sess, x, y)
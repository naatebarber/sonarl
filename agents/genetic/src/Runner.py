import tensorflow as tf
import numpy as np
from .SocketRelay import SocketRelay
import os
import time

class Runner:
    def __init__(self, sess, env, genetic, init_hidden_layers, init_layer_units, gaussian_noise, gen_size, num_attempts, sock, timestep=None):
        self.env = env
        self.sess = sess
        self.genetic = genetic
        self.gen_size = gen_size
        self.num_attempts_per_genetic = num_attempts
        self.sock = sock
        self.timestep = timestep
        # env layout
        self.num_states = self.env.get_num_states()
        self.num_actions = self.env.get_num_actions()
        # organism initial layout
        self.layers = init_hidden_layers
        self.units = init_layer_units
        self.noise = gaussian_noise
        # organisms
        self.gen = None
        self.gen_envs = None
        self.gen_ordi = None
        self.gen_fitness = None
        # refine
        self.last_gen_fittest = None
        self.total_fitness_store = []

    def run_gen(self):
        self.gen = []
        self.gen_fitness = []
        self.gen_ordi = []

        # generate envs for organisms
        self.gen_envs = []
        for i in range(self.gen_size):
            self.gen_envs.append(self.env())
            reset_ordi = self.gen_envs[i].reset()
            self.gen_ordi.append(reset_ordi)

        # generate organisms
        if self.last_gen_fittest is None:
            for i in range(self.gen_size):
                self.gen.append(
                    self.genetic(self.num_states, self.num_actions, self.layers, self.units, self.noise))
        else:
            for i in range(len(self.last_gen_fittest)):
                for _ in range(10):
                    self.gen.append(
                        self.last_gen_fittest[i].mutate())
        
        # populate fitness array
        self.gen_fitness = np.zeros([len(self.gen)])

        # run generation
        for _ in range(self.num_attempts_per_genetic):
            eliminated = 0
            while eliminated <= len(self.gen):
                if self.timestep is not None:
                    # only send visual updates if a timestep is enabled
                    time.sleep(self.timestep)
                    self.sock.send_step({
                        "env_action": "step",
                        "data": [None, float(np.sum(self.gen_fitness)), None]
                    })
                for i in range(len(self.gen_envs)):
                    if self.gen_ordi[i][2] is True:
                        continue

                    observation, reward, done = self.gen_envs[i].step(
                        self.gen[i].predict(
                            self.gen_ordi[i][0]))

                    self.gen_ordi[i] = [observation, reward, done]
                    self.gen_fitness[i] += reward

                    if done is True:
                        eliminated += 1

        # record total score
        self.total_fitness_store.append(np.sum(self.gen_fitness))

        # pull out top ten percent
        top = sorted([ (x, i) for (i, x) in enumerate(self.gen_fitness) ], reverse=True)
        self.last_gen_fittest = [ gen[i[1]] for i in top ]
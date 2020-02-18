import tensorflow as tf
import numpy as np
from .SocketRelay import SocketRelay
import os

class Runner:
    def __init__(self, sess, env, organism, init_hidden_layers, init_layer_units, gaussian_noise, gen_size, num_attempts):
        self.env = env
        self.sess = sess
        self.organism = organism
        self.gen_size = gen_size
        self.num_attempts_per_organism = num_attempts
        self.sock = SocketRelay(("localhost", int(os.getenv("SOCKET_SERVER_PORT"))))
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
                    self.organism(self.num_states, self.num_actions, self.layers, self.units, self.noise))
        else:
            for i in range(len(self.last_gen_fittest)):
                for _ in range(10):
                    self.gen.append(
                        self.last_gen_fittest[i].mutate())
        
        # populate fitness array
        self.gen_fitness = np.zeros([len(self.gen)])

        # run generation
        for _ in range(self.num_attempts_per_organism):
            eliminated = 0
            while eliminated <= len(self.gen):
                for i in range(len(self.gen_envs)):
                    if self.gen_ordi[i][2] is True:
                        continue

                    observation, reward, done = self.gen_envs[i].step(self.gen_ordi[i])
                    self.gen_ordi[i] = [observation, reward, done]
                    self.gen_fitness[i] += reward

                    if done is True:
                        eliminated += 1
                self.sock.send_step({
                    "env_action": "step",
                    "position": [[float(i) for i in e.position] for e in self.gen_envs]
                })

        # record total score
        self.total_fitness_store.append(np.sum(self.gen_fitness))
        self.sock.send_step({
            "env_action": "step",
            "data": [None, float(np.sum(self.gen_fitness)), None]
        })

        # pull out top ten percent
        top = sorted([ (x, i) for (i, x) in enumerate(self.gen_fitness) ], reverse=True)
        self.last_gen_fittest = [ gen[i[1]] for i in top ]
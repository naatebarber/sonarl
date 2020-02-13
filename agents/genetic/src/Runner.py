import tensorflow as tf
import numpy as np

class Runner:
    def __init__(self, sess, env, organism, init_hidden_layers, init_layer_units, gaussian_noise, gen_size):
        self.env = env
        self.sess = sess
        self.organism = organism
        self.gen_size = gen_size

        # env layout
        self.num_states = self.env.num_states
        self.num_actions = self.env.num_actions

        # organism initial layout
        self.layers = init_hidden_layers
        self.units = init_layer_units
        self.noise = gaussian_noise

        # organisms
        self.gen = None
        self.last_gen_fittest = None

        # fitness scores
        self.gen_fitness = []
        self.total_fitness_store = []

    def run_gen(self):
        self.env.reset()
        self.gen_fitness = []
        self.gen = []

        # generate organisms
        if self.last_gen_fittest is None:
            for i in range(self.gen_size):
                self.gen.append(
                    organism(self.num_states, self.num_actions, self.layers, self.units, self.noise))
        else:
            for i in range(len(self.last_gen_fittest)):
                for _ in range(10):
                    self.gen.append(
                        self.last_gen_fittest[i].mutate())
        # run generation
        # (TODO) create env capable of hosting multple agents
        

        # record total score
        self.total_fitness_store.append(np.sum(self.gen_fitness))

        # pull out top ten percent
        top = sort([ (x, i) for (i, x) in enumerate(self.gen_fitness) ], reverse=True)
        self.last_gen_fittest = [ gen[i[1]] for i in top ]
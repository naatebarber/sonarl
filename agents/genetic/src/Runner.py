import tensorflow as tf
import numpy as np
from .SocketRelay import SocketRelay
import os
import time
import math

class Runner:
    def __init__(
            self, 
            env=None, 
            genetic=None, 
            init_hidden_layers=3, 
            init_layer_units=10, 
            gaussian_noise=0.2, 
            gen_size=100, 
            num_attempts=10, 
            sock=None, 
            timestep=None,
            cutoff=1000,
            skip=100):

        self.env = env
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
        self.generation = 0
        self.cutoff = cutoff
        self.skip = skip
        self.num_episodes = 0
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
                # 50 crossover genes and 50 noise mutated genes
                for _ in range(len(self.last_gen_fittest) * 10):
                    # if i > len(self.last_gen_fittest) * 5:
                    self.gen.append(
                        self.last_gen_fittest[i].mutate_with_noise())
                    # else:
                    #     # top fifty percent of the top ten percent
                    #     # top five percent
                    #     sample_space = self.last_gen_fittest[:int(np.floor((len(self.last_gen_fittest) / 2)))]
                    #     gene1 = np.random.choice(sample_space)
                    #     gene2 = np.random.choice(sample_space)
                    #     crossed_gene = (gene1.layer_random_cross(gene2)) if np.random.rand() < 0.5 else (gene2.layer_random_cross(gene1))
                    #     self.gen.append(crossed_gene)
        
        # populate fitness array
        self.gen_fitness = np.zeros([len(self.gen)])

        # run generation
        for _ in range(self.num_attempts_per_genetic):
            eliminated = 0
            n_steps = 0
            while True:
                n_steps += 1
                if self.timestep is not None and self.num_episodes > self.skip:
                    time.sleep(self.timestep)
                for i in range(len(self.gen_envs)):
                    if self.gen_ordi[i][2] is True:
                        # print("Genetic {} is dead".format(i))
                        continue

                    observation, reward, done = self.gen_envs[i].step(
                        int(np.argmax(
                            self.gen[i].predict(
                                self.gen_ordi[i][0]))))

                    self.gen_ordi[i] = [observation, reward, done]
                    self.gen_fitness[i] += reward

                    if done is True:
                        eliminated += 1
                        print("{} out of {} eliminated in generation {}".format(eliminated, len(self.gen), self.generation))
                if eliminated is self.gen_size or n_steps > self.cutoff: 
                    self.gen_ordi = []
                    for k in range(self.gen_size):
                        reset_ordi = self.gen_envs[k].reset()
                        self.gen_ordi.append(reset_ordi)
                    break
                if self.num_episodes > self.skip:
                    self.sock.send_step({
                        "env_action": "step",
                        "agent_type": "genetic",
                        "position": [[float(i) for i in e.position] for e in self.gen_envs]
                    })

        # record total score
        self.total_fitness_store.append(np.sum(self.gen_fitness))
        self.num_episodes += 1

        # pull out top ten percent
        top = sorted([ (x, i) for (i, x) in enumerate(self.gen_fitness) ], reverse=True)
        self.last_gen_fittest = [ self.gen[i[1]] for i in top ][:(math.floor(self.gen_size / 10))]
        print("Generation {} finished".format(self.generation))
        self.generation += 1
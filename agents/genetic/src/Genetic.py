import tensorflow as tf
import numpy as np

class Genetic:
    def __init__(self, num_states, num_actions, num_hidden=4, num_units=50, gamma=0.3, dense_layers=None):
        # define shapes
        self.num_states = num_states
        self.num_actions = num_actions
        self.num_hidden = num_hidden
        self.num_units = num_units
        # input placeholder
        self.states = None
        # hidden layers
        self.hidden = None
        self.action_layer = None
        self.logits = None
        # mutation rate
        self.gamma = gamma
        # mutated weights
        self.dense_layers = dense_layers
        # build model
        self.genes = self.define_genome()
        self.var_init = None

    def define_genome(self):
        self.states = tf.placeholder(tf.float32, shape=[None, self.num_states])
        self.hidden = []
        if self.dense_layers is None:
            for i in range(self.num_hidden):
                self.hidden.append(
                    tf.layers.Dense(
                        units=self.num_units,
                        activation=tf.nn.relu))
        else:
            self.hidden = self.dense_layers
        # action layer outputs logits
        self.action_layer = tf.layers.Dense(self.num_actions)

        # matrix feed for logits
        for i in range(len(self.hidden)):
            if i is 0:
                self.logits = self.hidden[i].apply(self.states)
            else:
                self.logits = self.hidden[i].apply(self.logits)

        # reshape to action
        self.logits = self.action_layer.apply(self.logits)
        self.var_init = tf.global_variables_initializer()

    def predict(self, sess, state):
        return sess.run(self.logits, {self.states: state})

    def mutate(self):
        pass
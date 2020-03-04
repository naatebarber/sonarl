import tensorflow as tf
import numpy as np
# Deprecated but still interesting
class GeneticTensor:
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
                if i is 0:
                    self.hidden.append({
                        "activation": tf.nn.relu,
                        "weight": tf.Variable(
                            initial_value=tf.random_normal([self.num_states, self.num_units]), 
                            dtype=tf.float32),
                        "bias": tf.Variable(
                            initial_value=tf.random_normal([self.num_states, self.num_units]), 
                            dtype=tf.float32)
                    })
                else:
                    self.hidden.append({
                        "activation": tf.nn.relu,
                        "weight": tf.Variable(
                            initial_value=tf.random_normal([self.num_units, self.num_units]), 
                            dtype=tf.float32),
                        "bias": tf.Variable(
                            initial_value=tf.random_normal([self.num_units, self.num_units]), 
                            dtype=tf.float32)
                    })
        else:
            self.hidden = self.dense_layers
        # action layer outputs logits
        self.action_layer = {
            "weight": tf.Variable(
                initial_value=tf.random_normal([self.num_units, self.num_actions]), 
                dtype=tf.float32),
            "bias": tf.Variable(
                initial_value=tf.random_normal([self.num_units, self.num_actions]), 
                dtype=tf.float32)
        }

        # matrix feed for logits
        for i in range(len(self.hidden)):
            if i is 0:
                self.logits = self.hidden[i].activation(tf.add(tf.matmul(self.states, self.hidden[i].weight), self.hidden[i].bias))
            else:
                self.logits = self.hidden[i].activation(tf.add(tf.matmul(self.logits, self.hidden[i].weight), self.hidden[i].bias))

        # reshape to action
        self.logits = tf.add(tf.matmul(self.logits, self.action_layer.weight), self.action_layer.bias)
        self.var_init = tf.global_variables_initializer()

    def predict(self, sess, state):
        return sess.run(self.logits, {self.states: state})

    def mutate(self):
        pass

    def cross(self):
        pass
import tensorflow as tf
import numpy as np

class Organism:
    def __init__(self, num_states, num_actions, num_hidden_layers, num_hidden_units, noise_level=0.7, parent_weights=None, parent_biases=None):
        # shapes
        self.num_states = num_states
        self.num_actions = num_actions
        self.num_hidden_layers = num_hidden_layers
        self.num_hidden_units = num_hidden_units

        # evolution
        self.noise_level = noise_level
        self.parent_weights = parent_weights
        self.parent_biases = parent_biases

        # placeholders
        self.states = None
        
        # hidden
        self.hidden_layers = []

        # output
        self.var_init = None
        self.logits = None
        self.model = self.define_model()

    def define_model(self):
        # define states
        self.states = tf.placeholder(tf.float32, [None, self.num_states], name="States")
        
        # define hidden layers
        if self.parent_biases is None and self.parent_weights is None:
            # init a random weight/bias for each hidden layer
            for i in range(self.num_hidden_layers):
                if i is 0:
                    self.hidden_layers.append(
                        tf.layers.dense(
                            self.states, 
                            self.num_hidden_units, 
                            tf.nn.relu,
                            reuse=tf.AUTO_REUSE,
                            name="hidden{}".format(i)))
                else:
                    self.hidden_layers.append(
                        tf.layers.dense(
                            self.hidden_layers[i - 1],
                            self.num_hidden_units,
                            tf.nn.relu,
                            reuse=tf.AUTO_REUSE,
                            name="hidden{}".format(i)))
        else:
            # Apply mutated parent weights to new instance
            for i in range(self.num_hidden_layers):
                if i is 0:
                    self.hidden_layers.append(
                        tf.layers.dense(
                            self.states, 
                            kernel_initializer=tf.get_variable("kernel"),
                            bias_initializer=tf.get_variable("bias"),
                            activation=tf.nn.relu,
                            reuse=tf.AUTO_REUSE,
                            name="hidden{}".format(i)))
                else:
                    self.hidden_layers.append(
                        tf.layers.dense(
                            self.states, 
                            kernel_initializer=tf.get_variable("kernel"),
                            bias_initializer=tf.get_variable("bias"),
                            activation=tf.nn.relu,
                            reuse=tf.AUTO_REUSE,
                            name="hidden{}".format(i)))

        # create output layer
        self.logits = tf.layers.dense(
            self.hidden_layers[self.num_hidden_layers - 1],
            self.num_hidden_units,
            name="logits")

        self.var_init = tf.global_variables_initializer()

    def predict(self, sess, states):
        return sess.run(self.logits, {self.states: states})

    def mutate_parent_layer(self, prev_layer, layer_name):
        # mutate parent matrix 
        pass

    def reduce_noise(self, delta):
        self.noise_level -= delta
        return self

    def mutate(self):
        # get matricies from hidden layers
        weights = []
        biases = []
        for i in range(len(self.hidden_layers)):
            with tf.get_variable_scope("hidden{}".format(i)):
                weights.append(tf.get_variable("kernel"))
                biases.append(tf.get_variable("bias"))
        # mutate matricies
        for i in range(len(self.num_hidden_layers)):
            w_max = tf.reduce_max(tf.abs(weights[i]))
            b_max = tf.reduce_max(tf.abs(biases[i]))
            w_dev = w_max * self.noise_level
            b_dev = b_max * self.noise_level
            w_noise = tf.random_normal(shape=tf.shape(weights[i]), mean=0., stddev=w_dev)
            b_noise = tf.random_normal(shape=tf.shape(biases[i]), mean=0., stddev=b_dev)
            weights[i] = tf.add(w_noise, weights[i])
            biases[i] = tf.add(b_noise, biases[i])
        # pass mutated matricies to new organism class instance
        child = Organism(
            self.num_states, 
            self.num_actions, 
            self.num_hidden_layers, 
            self.num_hidden_units,
            self.noise_level,
            weights, 
            biases)
        # return mutated organism
        return child

    def cross(self):
        # organism gene crossover (TODO)
        pass
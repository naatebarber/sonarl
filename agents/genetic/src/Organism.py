import tensorflow as tf
import numpy as np

class Organism:
    def __init__(self, num_states, num_actions, num_hidden_layers, num_hidden_units, mutate=0.7, parent_weights=None, parent_biases=None):
        # shapes
        self.num_states = num_states
        self.num_actions = num_actions
        self.num_hidden_layers = num_hidden_layers
        self.num_hidden_units = num_hidden_units

        # evolution
        self.mutate = mutate
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
                if len(self.hidden_layers) is 0:
                    self.hidden_layers.append(
                        tf.layers.dense(
                            self.states, 
                            self.num_hidden_units, 
                            tf.nn.relu,
                            name="hidden{}".format(i)))
                else:
                    self.hidden_layers.append(
                        tf.layers.dense(
                            self.hidden_layers[i - 1],
                            self.num_hidden_units,
                            tf.nn.relu,
                            name="hidden{}".format(i)))
        else:
            # utilize the mutate property to alter parent weight/bias for each hidden layer
            for i in range(self.num_hidden_layers):
                if len(self.hidden_layers) is 0:
                    self.hidden_layers.append(
                        self.mutate_parent_layer(
                            self.states,
                            "hidden{}".format(i)))
                else:
                    self.hidden_layers.append(
                        self.mutate_parent_layer(
                            self.hidden_layers[i - 1],
                            "hidden{}".format(i)))
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

    def mutate(self):
        # get matricies from hidden layers
        # mutate matricies
        # pass mutated matricies to new organism class instance
        # return mutated organism
        # lather rinse repeat
        pass
import tensorflow as tf
import numpy as np

class Model:
    def __init__(self, num_states, num_actions, batch_size):
        self._num_states = num_states
        self._num_actions = num_actions
        self._batch_size = batch_size
        # placeholders
        self._states = None
        self._actions = None
        # outputs
        self._logits = None
        self._optimizer = None
        self._var_init = None
        # model
        self._model = self.define_model()

    def define_model(self):
        # define placeholders
        self._states = tf.placeholder(tf.float32, shape=[None, self._num_states], name="States")
        self._q_s_a = tf.placeholder(tf.float32, shape=[None, self._num_actions], name="Actions")
        # define hidden layers
        hl1 = tf.layers.dense(self._states, 124, tf.nn.relu)
        hl2 = tf.layers.dense(hl1, 124, tf.nn.relu)
        hl3 = tf.layers.dense(hl2, 124, tf.nn.relu)
        self._logits = tf.nn.softmax(tf.layers.dense(hl3, self._num_actions, name="Prediction"))
        # define loss and optimizer
        loss = tf.losses.mean_squared_error(self._q_s_a, self._logits)
        self._optimizer = tf.train.AdamOptimizer().minimize(loss)
        self._var_init = tf.global_variables_initializer()

    def predict_one(self, state, sess):
        return sess.run(self._logits, {self._states: state.reshape([1, self._num_states])})

    def predict_batch(self, states, sess):
        return sess.run(self._logits, {self._states: states})

    def train_model(self, sess, x, y):
        return sess.run(self._optimizer, {self._states: x, self._q_s_a: y})
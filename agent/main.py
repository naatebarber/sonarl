import socket_handle
import env
import src
import os
import json
import tensorflow as tf
import numpy as np

if __name__ == "__main__":
    env_address = ("localhost", int(os.getenv("SOCKET_SERVER_PORT")))
    env = env.Env(env_address, {})
    print(env.sample_random_action())

    num_states = 6
    num_actions = 4
    batch_size = 10
    model = src.Model(num_states, num_actions, batch_size)

    max_memory = 10000
    memory = src.Memory(max_memory)

    num_episodes = 10

    with tf.Session() as sess:
        sess.run(model._var_init)
        runner = src.Runner(sess, env, model, memory, 0.8, 1e-5, .95)
        for i in range(num_episodes):
            runner.run()

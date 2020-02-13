from env import SonarWithAccelerometerBarometer
from env import EnvSocketWrapper
import src
import os
import json
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt

if __name__ == "__main__":
    env_worker = SonarWithAccelerometerBarometer()
    env_address = ("localhost", int(os.getenv("SOCKET_SERVER_PORT")))
    env = EnvSocketWrapper(env_address, env_worker)
    reset_ordi = env.reset()

    num_states = 6
    num_actions = 4
    batch_size = 10
    model = src.Model(env_worker.num_states, env_worker.num_actions, batch_size)

    max_memory = 10000
    memory = src.Memory(max_memory)

    num_episodes = 100

    with tf.Session() as sess:
        sess.run(model._var_init)
        runner = src.Runner(sess, env, model, memory, 0.8, 1e-5, .97, 0)
        for i in range(num_episodes):
            runner.run()
            if i % 10 == 0:
                print("EPISODE {}".format(i))
        # # plot reward growth
        # plt.plot(runner._reward_store)
        # plt.show()
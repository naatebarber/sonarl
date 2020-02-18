import tensorflow as tf
import numpy as np
from agents.genetic.src.SocketRelay import SocketRelay
from agents.genetic.src.Genetic import Genetic
from agents.genetic.src.Runner import Runner
import os
from env import SonarWithAccelerometerBarometer as Sonar
import env
from matplotlib import pyplot as plt

if __name__ == "__main__":
    num_episodes = 100

    with tf.Session() as sess:
        runner = Runner(sess, Sonar, Genetic, 4, 50, 0.1, 100, 10, SocketRelay(("localhost", int(os.getenv("SOCKET_SERVER_PORT")))), timestep=0.01)
        for i in range(num_episodes):
            runner.run_gen()
        plt.plot(runner.total_fitness_store)
        plt.show()
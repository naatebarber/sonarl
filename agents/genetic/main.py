import tensorflow as tf
import numpy as np
import src
from env import SonarWithAccelerometerBarometer as Sonar
import env
from matplotlib import pyplot as plt

if __name__ == "__main__":
    num_episodes = 100

    with tf.Session() as sess:
        runner = src.Runner(sess, Sonar, src.Genetic, 4, 50, 0.1, 100, 10)
        for i in range(num_episodes):
            runner.run_gen()
        plt.plot(runner.total_fitness_store)
        plt.show()
import tensorflow as tf
import numpy as np
from agents.genetic.src.SocketRelay import SocketRelay
from agents.genetic.src.Genetic import Genetic
from agents.genetic.src.Runner import Runner
import os
from env import SonarWithAccelerometerBarometer as Sonar
import env
# from matplotlib import pyplot as plt

if __name__ == "__main__":
    num_episodes = 100

    runner = Runner(
        env=Sonar, 
        genetic=Genetic, 
        init_hidden_layers=4, 
        init_layer_units=50, 
        gaussian_noise=0.1, 
        gen_size=100,
        num_attempts=1,
        sock=SocketRelay(("localhost", int(os.getenv("SOCKET_SERVER_PORT")))),
        timestep=0.05)
        
    for i in range(num_episodes):
        runner.run_gen()
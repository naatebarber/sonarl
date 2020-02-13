import socket
import json

class EnvSocketWrapper:
    def __init__(self, address, env):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(address)
        self.env = env

    def step(self, action):
        ordi = self.env.step(action)
        self.socket.send(bytes(json.dumps({
            "env_action": "step",
            "data": ordi,
            "position": [ float(i) for i in self.env.position ]
        }), "utf-8"))
        return ordi

    def reset(self):
        ordi = self.env.reset()
        self.socket.send(bytes(json.dumps({
            "env_action": "reset",
            "data": ordi
        }), "utf-8"))
        return ordi

    def sample_random_action(self):
        return self.env.sample_random_action()

    def observation_space(self):
        return self.env.ordi()

    
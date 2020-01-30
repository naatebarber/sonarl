import socket_handle
import json

class Env:
    def __init__(self, address, params={}):
        self.socket = socket_handle.Socket()
        self.socket.connect(address)

    def reset(self):
        self.socket.send_data(json.dumps({
            'env_action': "reset",
            'params': {}
        }))

    def step(self, action):
        if isinstance(action, dict): action = json.dumps(action)
        self.socket.send_data(bytes(json.dumps({
            'env_action': "step",
            'params': {
                'action': action
            }
        }), "utf-8"))
        res_bytes = self.socket.recv_data()
        res = res_bytes.decode("utf-8")
        res_dict = json.loads(res)
        return res_dict

    def observation_space(self):
        self.socket.send_data(json.dumps({
            'env_action': "get_observation",
            'params': {}
        }))
import socket_handle
import json

class Env:
    def __init__(self, address, params={}):
        self.socket = socket_handle.Socket()
        self.socket.connect(address)

    def reset(self):
        self.socket.send_data(bytes(json.dumps({
            'env_action': 'reset',
            'params': None
        }), "utf-8"))
        res_reset = self.socket.recv_data()
        res = res_reset.decode("utf-8")
        res_dict = json.loads(res)
        return res_dict['ordi']

    def step(self, action):
        try:
            action = action.tolist()
        except:
            pass
        if isinstance(action, dict): action = json.dumps(action)
        self.socket.send_data(bytes(json.dumps({
            'env_action': 'step',
            'params': {
                'action': action
            }
        }), "utf-8"))
        res_step = self.socket.recv_data()
        res = res_step.decode("utf-8")
        res_dict = json.loads(res)
        return res_dict['ordi']

    def observation_space(self):
        self.socket.send_data(bytes(json.dumps({
            'env_action': 'get_observation',
            'params': None
        }), "utf-8"))
        res_obs = self.socket.recv_data()
        res = res_obs.decode("utf-8")
        res_dict = json.loads(res)
        return res_dict['ordi']

    def sample_random_action(self):
        self.socket.send_data(bytes(json.dumps({
            'env_action': 'sample_random_action',
            'params': None
        }), "utf-8"))
        res_sample = self.socket.recv_data()
        res = res_sample.decode("utf-8")
        res_dict = json.loads(res)
        return res_dict['ordi']
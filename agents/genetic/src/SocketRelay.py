import socket
import json

class SocketRelay:
    def __init__(self, address):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(address)

    def send_step(self, dict):
        self.socket.send(bytes(json.dumps(dict), "utf-8"))
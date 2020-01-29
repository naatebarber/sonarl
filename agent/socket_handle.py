import socket as sock

class Socket:
    def __init__(self):
        self.client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    def connect(self, addr):
        self.client.connect(addr)

    def send_data(self, data):
        self.client.send(data)

    def close(self):
        self.client.close()

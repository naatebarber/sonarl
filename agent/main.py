import socket_handle
import src
import os


if __name__ == "__main__":
    sock_cli = socket_handle.Socket()
    sock_cli.connect(("localhost", int(os.getenv("SOCKET_SERVER_PORT"))))
    sock_cli.send_data(b"Hello")

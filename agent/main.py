import socket_handle
import env
import src
import os


if __name__ == "__main__":
    env_address = ("localhost", int(os.getenv("SOCKET_SERVER_PORT")))
    env = env.Env(env_address, {})
    step_res = env.reset()
    print(step_res)
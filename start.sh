#!/bin/bash

source .env
yarn
pip install -r requirements.txt
screen -dm -S NODE_ENV node index.js
echo "Node ENV server running as screen daemon. Supervise with 'screen -xS NODE_ENV'"
screen -ls
echo "To run a simulation: (python agent/main.py)"
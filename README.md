# sonarl  
Temporal difference learning with Deep Q Network, utilizing experience replay

### index.js  
Websocket server for connecting agent updates to web interface and connective mesh.  

### src/socket.js  
Env-agent communication handler. Updates websockets with recent data and activates env methods.

### src/env.js  
Contains an object containing different environment classes and methods.

### client/*  
Client code for displaying environment and success of DQN

### agent/*.py
Python package for handling socket connections, translating values to agent-readable format, and running DQN on observations.

## Current ENV Observation/Actions/Reward/Done   
O: 6 'sonar' values, `((1, front), (2, left), (3, right), (4, back), (5, top), (6, bottom))`  
A: Array of four floats, each representing change in TPRY `((1, throttle), (2, pitch), (3, roll), (4, yaw))`  
R: `Math.pow(1 - (((this.map_size / 2) % i) || 0.01) / (this.map_size / 2), 2)` - mean of dimensional vectors   
D: Agent exceeds max_distance_from_center  

## Running the simulation  
Run the simulation using the start script `./start.sh`  
This will install all node/python packages and start the node socket/env server inside a screen daemon.
Following this, run `agent/main.py` to experiment with the RL.

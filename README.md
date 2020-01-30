# sonarl  
Sonar based autopilot simulation

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
A: Array of four floats, each representing change in motor power `((1, front-left), (2, front-right), (3, back-right), (4, back-left))`  
R: `(distance_from_center / max_distance_from_center) ^ 2`  
D: Agent exceeds max_distance_from_center  
# sonarl  
Temporal difference learning with Deep Q Network, utilizing experience replay

### index.js  
Websocket server for connecting agent updates to web reporting interface.  

### src/socket.js  
Env-agent communication handler. Updates websockets with recent data.

### env/*  
Python env. Currently only contains SonarWithAccelerometerAndBarometer which assumes automatic adjustment to gravity and tilt.  
Also includes EnvSocketWrapper, which adds a socket relay to env method calls.

### client/*  
Client code for displaying environment and success of DQN/GenAlg.

### agent/deep_q   
Deep Q Network with experience replay  

### agent/genetic   
Genetic algorithm mutated by gaussian noise. Crossover mutations (WIP)  

## Current ENV Observation/Actions/Reward/Done   
O: 6 'sonar' values, `((1, front), (2, left), (3, right), (4, back), (5, top), (6, bottom))`  
A: One-hot shape (9) Array `throttle_up, throttle_down, roll_pos, roll_neg, pitch_pos, pitch_neg, yaw_pos, yaw_neg, no_action`    
R: `-10 if new position is farther than old position, +10 vice versa` 
D: Agent exceeds max_distance_from_center  

## Running the simulation  
Run the simulation using the start script `./start.sh`  
This will install all node/python packages and start the node socket/env server inside a screen daemon.
Following this, run `agent/{genetic || deep_q}/main.py` to experiment with the RL.

View space simulation (THREE) and reward graphs (D3) at `localhost:8080`

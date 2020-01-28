# sonarl  
Sonar based autopilot simulation

### env.js  
Contains an object containing different environment classes.

### index.js  
Websocket server for connecting agent updates to web interface.  
Endpoints for env operations

### agent/*.py
Python package for handling socket connections, translating values to agent-readable format, and running DQN on observations.
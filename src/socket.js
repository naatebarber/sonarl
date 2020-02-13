const net = require("net");

const initializeSocketServer = conf => {
    const sockServer = net.createServer();
    sockServer
        .on("connection", sock => {
            sock.on("data", packet => {
                try {
                    var { graphWs, threeWs } = conf;
                    const { env_action, data, position } = JSON.parse(packet.toString("utf-8"));
                    console.log(env_action, data, position);
                    

                    if(env_action == "step") {
                        if(graphWs && typeof data[1] == "number") graphWs.send(JSON.stringify({
                            graph: {
                                reward: Math.floor( 1000 * data[1] ) / 1000
                            }
                        }));
                        if(threeWs) threeWs.send(JSON.stringify({
                            vector: position
                        }));
                    }
                } catch(err) {
                    console.log("Error recv agent-sock data: " + err)
                }
            });
        })
        .listen(process.env.SOCKET_SERVER_PORT, null, null, () => {
            console.log("Socket server listening on " + process.env.SOCKET_SERVER_PORT)
        });
    return sockServer;
}

module.exports = initializeSocketServer;
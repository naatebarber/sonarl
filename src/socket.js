const net = require("net");
var totalReward = 0;

const initializeSocketServer = conf => {
    const sockServer = net.createServer();
    sockServer
        .on("connection", sock => {
            sock.on("data", packet => {
                try {
                    var { graphWs, threeWs } = conf;
                    const { env_action, data, position } = JSON.parse(packet.toString("utf-8"));
                    // data  = [observation, reward, done]
                    if(env_action == "step") {

                        let graphData = {
                            graph: {
                                reward: Math.floor( 1000 * data[1] ) / 1000,
                            }
                        }

                        let threeData = {
                            vector: Array.isArray(position[0]) ? position : [position],
                            done: data[2]
                        }

                        if(data[2] == false) {
                            totalReward += data[1];
                        } else {
                            graphData.graph.totalReward = totalReward
                            totalReward = 0;
                        }

                        if(graphWs && typeof data[1] == "number") graphWs.send(JSON.stringify(graphData));
                        if(threeWs) threeWs.send(JSON.stringify(threeData));
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
const net = require("net");

const initializeSocketServer = conf => {
    const sockServer = net.createServer();
    sockServer
        .on("connection", sock => {
            sock.on("data", packet => {
                try {
                    var { ws } = conf;

                    const { env_action, data } = JSON.parse(packet.toString("utf-8"));
                    console.log(env_action, data);

                    if(ws && env_action == "step") ws.send(JSON.stringify({
                        graph: {
                            reward: [data.ordi[1]]
                        }
                    }))
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
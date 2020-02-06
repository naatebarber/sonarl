const net = require("net");

const initializeSocketServer = conf => {
    const sockServer = net.createServer();
    sockServer
        .on("connection", sock => {
            sock.on("data", data => {
                try {
                    var { ws } = conf;

                    const { env_action, data } = JSON.parse(data.toString("utf-8")),
                        ordi = data.ordi;

                    if(ws && env_action == "step") ws.send(JSON.stringify({
                        graph: {
                            reward: [ordi[1]]
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
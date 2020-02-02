const net = require("net"),
    envlib = require("./env"),
    commandMap = envlib.envCommandMap;

const initializeSocketServer = conf => {
    const sockServer = net.createServer();
    sockServer
        .on("connection", sock => {
            sock.on("data", data => {
                try {
                    var { env, ws } = conf;

                    const { env_action, params } = JSON.parse(data.toString("utf-8"));
                    const ordi = commandMap(env)(env_action, params);

                    sock.write(Buffer.from(JSON.stringify({
                        env_action: env_action,
                        success: Array.isArray(ordi),
                        ordi: ordi
                    })));

                    if(ws && env_action == "step") ws.send(JSON.stringify({
                        env_action: env_action,
                        action: params,
                        position: env.position,
                        map_size: env.map_size
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
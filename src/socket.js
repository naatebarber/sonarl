const net = require("net");

const initializeSocketServer = conf => {
    const sockServer = net.createServer();
    sockServer
        .on("connection", sock => {
            sock.on("data", data => {
                const ws = conf.subscribews;
                if(ws) ws.send(data.toString("utf-8"))
                    
                const stringData = data.toString("utf-8");
                console.log(stringData);
                sock.write(Buffer.from(JSON.stringify({
                    did: "Get your data"
                })))
            });
        })
        .listen(process.env.SOCKET_SERVER_PORT, null, null, () => {
            console.log("Socket server listening on " + process.env.SOCKET_SERVER_PORT)
        });
    return sockServer;
}

module.exports = initializeSocketServer;
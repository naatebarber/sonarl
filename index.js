const express = require("express"),
    net = require("net"),
    app = express(),
    env = require("./env"),
    expressws = require("express-ws")(app);

app.use(express.static(__dirname + "/ui"))
    .ws("/gui", (ws, req) => {
        console.log("Connection made");
        ws.send("ws available")
        ws.send("another");
    })
    .get("/env", (req, res) => {
        
    })
    .listen(process.env.GUI_PORT, () => console.log("GUI running on " + process.env.GUI_PORT))

function initialize() {
    const sockServer = net.createServer();
    sockServer.on("connection", sock => {
            sock.on("data", data => {
                const stringData = data.toString("utf-8");
                console.log(stringData);
                sock.write(Buffer.from(JSON.stringify({
                    did: "Get your data"
                })))
            });
        }).listen(process.env.SOCKET_SERVER_PORT, null, null, () => {
            console.log("Socket server listening on " + process.env.SOCKET_SERVER_PORT)
        });
}

initialize();
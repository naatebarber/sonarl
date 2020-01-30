const express = require("express"),
    net = require("net"),
    app = express(),
    envlib = require("./env"),
    expressws = require("express-ws")(app),
    bodyparser = require("body-parser"),
    socketServer = initializeSocketServer(),
    envs = [];

app.use(express.static(__dirname + "/ui"))
    .use(bodyparser.json())
    .use(bodyparser.urlencoded({extended: false}))
    .ws("/gui", (ws, req) => {
        console.log("Connection made");
        ws.send("ws available")
        ws.send("another");
    })
    .post("/init-env", (req, res) => {
        // GUI ENV Generation endpoint WIP
        console.log(req.body);
        let selectedEnv = req.body.env;
        if(!Object.keys(envlib).includes(selectedEnv)) return res.send(`Options include [${Object.keys(envlib).join()}]`)
        env = { name: selectedEnv, index: envs.length + 1, env: new envlib[selectedEnv]() }
        envs.push(env);
    })
    .listen(process.env.GUI_PORT, () => console.log("GUI running on " + process.env.GUI_PORT))

const initializeSocketServer = () => {
    const sockServer = net.createServer();
    sockServer
        .on("connection", sock => {
            sock.on("data", data => {
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

const envCommandMap = env => (command, params) => {
    switch(command) {
        case "reset":
            return env.reset();
        case "step":
            return env.step(params);
        case "get_observation":
            return env.get_observation();
        default: return null;
    }
}
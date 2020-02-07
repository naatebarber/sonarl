const express = require("express"),
    net = require("net"),
    spawn = require("child_process").spawn,
    app = express(),
    initSocket = require("./src/socket"),
    expressws = require("express-ws")(app),
    bodyparser = require("body-parser"),
    socketServerConf = {
        ws: undefined
    }
    socketServer = initSocket(socketServerConf);

app.use(express.static(__dirname + "/ui"))
    .use(bodyparser.json())
    .use(bodyparser.urlencoded({extended: false}))
    .ws("/gui", (ws, req) => {
        socketServerConf.ws = ws;
        console.log("Connection made");
    })
    .post("/run-agent", (req, res) => {
        let agentSession = spawn("python", [__dirname + "/agent/main.py"]),
            log = '';
        agentSession.stdout.on("data", data => log += data.toString("utf-8").replace(/\n/g, "<br>"))
        agentSession.on("exit", () => {
            res.send(log);
        });
    })
    .listen(process.env.GUI_PORT, () => console.log("GUI running on " + process.env.GUI_PORT))
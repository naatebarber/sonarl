const express = require("express"),
    net = require("net"),
    spawn = require("child_process").spawn,
    app = express(),
    envlib = require("./src/env"),
    initSocket = require("./src/socket"),
    expressws = require("express-ws")(app),
    bodyparser = require("body-parser"),
    socketServerConf = {
        env: new envlib.SonarEnv(200, 50, Math.PI / 18, 1),
        ws: undefined
    }
    socketServer = initSocket(socketServerConf),
    envs = [];

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
    .post("/init-env", (req, res) => {
        // GUI ENV Generation endpoint WIP
        console.log(req.body);
        let selectedEnv = req.body.env;
        if(!Object.keys(envlib).includes(selectedEnv)) return res.send(`Options include [${Object.keys(envlib).join()}]`)
        env = { name: selectedEnv, index: envs.length + 1, env: new envlib[selectedEnv]() }
        envs.push(env);
    })
    .listen(process.env.GUI_PORT, () => console.log("GUI running on " + process.env.GUI_PORT))
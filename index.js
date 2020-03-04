const express = require("express"),
    net = require("net"),
    spawn = require("child_process").spawn,
    app = express(),
    initSocket = require("./src/socket"),
    expressws = require("express-ws")(app),
    bodyparser = require("body-parser"),
    socketServerConf = {
        graphWs: undefined,
        threeWs: undefined
    }
    socketServer = initSocket(socketServerConf);

app.use(express.static(__dirname + "/ui"))
    .use(bodyparser.json())
    .use(bodyparser.urlencoded({extended: false}))
    .ws("/graph", (ws, req) => {
        socketServerConf.graphWs = ws;
        console.log("Graph connection made");
    })
    .ws("/simulate", (ws, req) => {
        socketServerConf.threeWs = ws;
        console.log("Simulation connection made");
    })
    .get("/three-orbit", (req, res) => {
        res.sendFile(__dirname + "/node_modules/three-orbitcontrols/OrbitControls.js")
    })
    .get("/three", (req, res) => {
        res.sendFile(__dirname + "/node_modules/three/src/Three.js")
    })
    .listen(process.env.GUI_PORT, () => console.log("GUI running on " + process.env.GUI_PORT))
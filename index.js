const express = require("express"),
    app = express(),
    env = require("./env"),
    expressws = require("express-ws")(app);

app.use(express.static(__dirname + "/ui"))
    .ws("/update", (ws, req) => {
        console.log("Connection made");
        ws.send("ws available")
        ws.send("another");
    })
    .get("/env", (req, res) => {
        
    })
    .listen(process.env.GUI_PORT, () => console.log("GUI running on " + process.env.GUI_PORT))
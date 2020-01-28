const express = require("express"),
    app = express(),
    expressws = require("express-ws")(app);

app.use(express.static(__dirname + "/ui"))
    .ws("/update", (ws, req) => {
        console.log("Connection made");
        ws.send("ws available")
    })
    .listen(process.env.GUI_PORT, () => console.log("GUI running on " + process.env.GUI_PORT))
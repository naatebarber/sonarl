$(document).ready(() => {
    $(".run-agent span").on("click", () => {
        $.post("/run-agent", data => {
            $(".run-agent-log").css("display", "block").html(data)
            $(".run-agent").remove()
        }); 
    });

    // D3 Graph
    var graphWs = new WebSocket("ws://localhost:8080/graph", "protocolOne"),
        store = {},
        svgParams = {
            w: (window.innerWidth / 1.5) < 600 ? (window.innerWidth / 1.5) : 600,
            h: (window.innerWidth / 1.5) < 600 ? (window.innerWidth / 1.5) : 600,
            m: 40
        },
        svg = {};
    graphWs.onmessage = (ev) => {
        recvNewDataPoint(store)(svg, svgParams)(ev)
    }

    // THREE simulation
    var threeWs = new WebSocket("ws://localhost:8080/simulate", "protocolOne")
    window.nodes = []
    threeWs.onmessage = (ev) => {
        let data = JSON.parse(ev.data),
            done = data.done;
        window.vectors = data.vector;
        if(done) {
            window.vectors = [];
        }
    }
});
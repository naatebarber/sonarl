$(document).ready(() => {
    var ws = new WebSocket("ws://localhost:8080/gui", "protocolOne"),
        graph = createGraph();
    ws.onmessage = updateGraph(graph)
});

const createGraph = () => {
    // create d3 graph
}

const updateGraph = graph => ev => {
    let data = unpackMessage(ev);
    // update graph
}

const unpackMessage = ev => {
    try {
        return JSON.parse(ev.data);
    } catch(e) {
        return ev.data
    }
}
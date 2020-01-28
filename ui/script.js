window.onload = () => {
    var socket = new WebSocket("ws://localhost:8080/update", "protocolOne");
    socket.onmessage = ev => {
        console.log(ev);
    }
}
window.onload = () => {
    xyzpos = new Array(3);

    var socket = new WebSocket("ws://localhost:8080/gui", "protocolOne");
    socket.onmessage = ev => {
        let data = undefined;
        try {
            data = JSON.parse(ev.data);
        } catch(err) {
            data = ev.data;
        }
        console.log(data);
    }
}
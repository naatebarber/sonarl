window.onload = () => {
    xyzpos = new Array(3);
    cv_xz = document.getElementById("xz");
    cx_xz = cv_xz.getContext("2d");
    cv_y = document.getElementById("y");
    cx_y = cv_y.getContext("2d");

    var socket = new WebSocket("ws://localhost:8080/gui", "protocolOne");
    socket.onmessage = ev => {
        let data = undefined;
        try {
            data = JSON.parse(ev.data);
        } catch(err) {
            data = ev.data;
        }
        console.log(data);
        if(typeof data == "object" && data.env_action && data.env_action == "step") {
            if(Array.isArray(data.position) && data.position.length == 3 && data.map_size) {
                drawPointWithScale(data.map_size, data.position[0], null, data.position[2], cx_xz, cv_xz);
                drawPointWithScale(data.map_size, null, data.position[1], null, cx_y, cv_y);
            }
        }
        console.log(data);
    }
}

function drawPointWithScale(max, currentx, currenty, currentz, cx, canvas) {
    let canvasWidth = canvas.width;
    let canvasHeight = canvas.height;
    let graphx = (currentx * canvasWidth) / max;
    let graphy = (currenty * canvasHeight) / max;
    let graphz = (currentz * canvasHeight) / max;
    cx.clearRect(0, 0, canvasWidth, canvasHeight);
    if(currentx && currentz) {
        cx.fillStyle = "blue";
        cx.fillRect(currentx, currentz, 3, 3);
    } else if(currenty) {
        cx.fillStyle = "red"
        cx.fillRect(canvasWidth / 2, currenty, 3, 3);
    }
}
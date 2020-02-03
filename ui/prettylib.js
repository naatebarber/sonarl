const handleMouse = e => params => {
    e.on("mousemove", (d, i) => {
        var [x, y] = d3.mouse(e.node())
        var [w, h] = [e.style("width"), e.style("height")].map(el => parseInt(el.replace("px", "")))
        var rx = x/w - 0.5
        var ry = y/h - 0.5
    })
}
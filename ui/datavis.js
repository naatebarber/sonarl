$(document).ready(() => {
    var ws = new WebSocket("ws://localhost:8080/gui", "protocolOne"),
        store = {
            positions: [[0,0,0]]
        },
        svg = createLineGraph(window.innerWidth / 1.5, window.innerWidth / 1.5, 40, store.positions);
        
    ws.onmessage = updateGraph(svg)(store)
});

const createLineGraph = (w, h, margin, data) => {
    // create d3 graph
    this.w = w;
    this.h = h;

    let svg = d3.select("svg")
    svg.transition().style("background-color", "#efefef").attr("width", `${w + margin * 2}px`).attr("height", `${h + margin * 2}px`)
    svg = svg.append("g").attr("transform", `translate(${margin}, ${margin})`)
    
    let xscale = d3.scaleLinear().domain([0, data.length]).range([0, w])
    let yscale = d3.scaleLinear().domain([0, data.reduce((a, b) => (a > b) ? a : b)]).range([h, 0])

    let line = d3.line().x((d, i) => xscale(i)).y(d => yscale(d)).curve(d3.curveMonotoneX)

    let axisX = d3.axisBottom(xscale)
    let axisY = d3.axisLeft(yscale)

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", `translate(0, ${h})`)
        .call(axisX)

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", `translate(0, 0)`)
        .call(axisY)

    svg.append("path")
        .datum(data)
        .attr("class", "line lx")
        .attr("d", line);

    svg.append("path")
        .datum(data)
        .attr("class", "line ly")
        .attr("d", line);
    
    svg.append("path")
        .datum(data)
        .attr("class", "line lz")
        .attr("d", line);

    return svg;
}

const updateGraph = svg => store => ev => {
    let data = recvNewDataPoint(ev)(store);
    console.log(data)
    data = data.positions
    data_x = data.map(e => e[0])
    data_y = data.map(e => e[1])
    data_z = data.map(e => e[2])
    let max = Math.max(...(data_x.concat(data_y).concat(data_z)))
    let min = Math.min(...(data_x.concat(data_y).concat(data_z)))

    let xscale = d3.scaleLinear().domain([0, data.length - 1]).range([0, w])
    let yscale = d3.scaleLinear().domain([min, max]).range([h, 0])
    let line = d3.line().x((d, i) => xscale(i)).y(d => yscale(d)).curve(d3.curveMonotoneX)

    svg.selectAll("g.x.axis")
        .call(d3.axisBottom(xscale))
    
    svg.selectAll("g.y.axis")
        .call(d3.axisLeft(yscale))

    svg.selectAll(".line.lx")
        .datum(data_x)
        .attr("d", line)
    
    svg.selectAll(".line.ly")
        .datum(data_y)
        .attr("d", line)
    
    svg.selectAll(".line.lz")
        .datum(data_z)
        .attr("d", line)
}

const recvNewDataPoint = ev => store => {
    try {
        let data = JSON.parse(ev.data);
        store.positions.push(data.position)
        return store;
    } catch(e) {
        return store;
    }
}
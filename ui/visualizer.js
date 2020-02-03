$(document).ready(() => {
    var ws = new WebSocket("ws://localhost:8080/gui", "protocolOne"),
        store = {},
        svgParams = {
            w: (window.innerWidth / 1.5) < 600 ? (window.innerWidth / 1.5) : 600,
            h: (window.innerWidth / 1.5) < 600 ? (window.innerWidth / 1.5) : 600,
            m: 40
        },
        svg = {};
        
    ws.onmessage = recvNewDataPoint(store)(svg, svgParams)
});

const createLineGraph = (w, h, margin, name) => {
    // create d3 graph
    this.w = w;
    this.h = h;

    d3.select(".vis").append("svg").attr("class", `svg-${name}`)

    let svg = d3.select(`svg.svg-${name}`)
    svg.transition().style("background-color", "#efefef").attr("width", `${w + margin * 2}px`).attr("height", `${h + margin * 2}px`)
    svg = svg.append("g").attr("transform", `translate(${margin}, ${margin})`)

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", `translate(0, ${h})`)

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", `translate(0, 0)`)

    svg.append("path")
        .attr("class", "line l0")

    svg.append("path")
        .attr("class", "line l1")
    
    svg.append("path")
        .attr("class", "line l2")

    return svg;
}

const updateGraph = svg => data => {

    console.log(data)
    // Where data is a 2d array [[][][][]]
    
    let max = Math.max(...data.flat())
    let min = Math.min(...data.flat())
    let reshaped = Array.apply(null, Array(3)).map(e => [])
    for(let i = 0; i < reshaped.length; i++) {
        for(let j = 0; j < data.length; j++) {
            reshaped[i].push(data[j][i]);
        }
    }
    data = reshaped;

    let xscale = d3.scaleLinear().domain([0, data[0].length - 1]).range([0, w])
    let yscale = d3.scaleLinear().domain([min, max]).range([h, 0])
    let line = d3.line().x((d, i) => xscale(i)).y(d => yscale(d)).curve(d3.curveMonotoneX)

    svg.selectAll("g.x.axis")
        .call(d3.axisBottom(xscale))
    
    svg.selectAll("g.y.axis")
        .call(d3.axisLeft(yscale))

    for(i = 0; i < data.length; i++) {
        svg.selectAll(`.line.l${i}`)
            .datum(data[i])
            .attr("d", line)
    }

    console.log("Updated!")
}

const recvNewDataPoint = store => (svg, params) => ev => {
    try {
        let data = JSON.parse(ev.data);
        Object.keys(data.graph).map(el => {
            if(store.hasOwnProperty(el)) {
                store[el].push(data.graph[el])
            } else {
                store[el] = [];
                store[el].push(data.graph[el])
            }
        });
        for(let i in store) {
            if(!(svg.hasOwnProperty(i))) svg[i] = createLineGraph(params.w, params.h, params.m, i);
            updateGraph(svg[i])(store[i])
        }
    } catch(e) {
        console.log(e)
        console.log(ev.data)
    }
    console.log(store);
    return store;
}
const createLineGraph = (w, h, margin, name) => {
    // create d3 graph
    this.w = w;
    this.h = h;

    d3.select(".vis").append("svg").attr("class", `svg-${name}`)

    let svg = d3.select(`svg.svg-${name}`)
    svg.transition().style("background-color", "#efefef").attr("width", `${w + margin * 2}px`).attr("height", `${h + margin * 2}px`)
    svg = svg.append("g").attr("transform", `translate(${margin}, ${margin})`)

    svg.append("text")
        .attr("x", 0)
        .attr("y", 0)
        .style("font-size", "22px")
        .style("margin-bottom", "22px")

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", `translate(0, ${h + 20})`)

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", `translate(0, 20)`)

    svg.append("path")
        .attr("class", "line l0")
        .attr("transform", `translate(0, 20)`)

    svg.append("path")
        .attr("class", "line l1")
        .attr("transform", `translate(0, 20)`)
    
    svg.append("path")
        .attr("class", "line l2")
        .attr("transform", `translate(0, 20)`)

    return svg;
}

const updateGraph = svg => data => title => {
    // Where data is a 2d array [[][][][]]
    
    let max = Math.max(...data.flat())
    let min = Math.min(...data.flat())
    if(Array.isArray(data[0])) {
        let reshaped = Array.apply(null, Array(3)).map(e => [])
        for(let i = 0; i < reshaped.length; i++) {
            for(let j = 0; j < data.length; j++) {
                reshaped[i].push(data[j][i]);
            }
        }
        data = reshaped;
    } else {
        data = [data]
    }

    let xscale = d3.scaleLinear().domain([0, data[0].length - 1]).range([0, w])
    let yscale = d3.scaleLinear().domain([min, max]).range([h, 0])
    let line = d3.line().x((d, i) => xscale(i)).y(d => yscale(d)).curve(d3.curveMonotoneX)

    svg.selectAll("text")
        .text(title)

    svg.selectAll("g.x.axis")
        .call(d3.axisBottom(xscale))
    
    svg.selectAll("g.y.axis")
        .call(d3.axisLeft(yscale))

    for(i = 0; i < data.length; i++) {
        svg.selectAll(`.line.l${i}`)
            .datum(data[i])
            .attr("d", line)
    }
}

const recvNewDataPoint = store => (svg, params) => ev => {
    try {
        let data = JSON.parse(ev.data);
        Object.keys(data.graph).map(el => {
            if(store.hasOwnProperty(el) && typeof data.graph[el] == "number") {
                store[el].push(data.graph[el])
            } else {
                store[el] = [];
                store[el].push(data.graph[el]);
            }
            while(store[el].length > 1000) store[el].shift();
        });
        for(let i in store) {
            if(!(svg.hasOwnProperty(i))) svg[i] = createLineGraph(params.w, params.h, params.m, i);
            updateGraph(svg[i])(store[i])(i)
        }
    } catch(e) {
        console.log(e)
        console.log(ev.data)
    }
    return store;
}
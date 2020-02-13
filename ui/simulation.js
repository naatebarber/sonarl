// Use THREE to simulate agent actions

const initThree = (domHandle, w, h) => {
    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(120, w / h, 0.1, 1000)
    var renderer = new THREE.WebGLRenderer()
    renderer.setSize(w, h)
    domHandle.append(renderer.domElement)
    var orbit = new THREE.OrbitControls(camera, renderer.domElement)
    return { scene, camera, renderer }
}

const sphere = () => {
    let geo = new THREE.SphereGeometry(10, 100, 100)
    let material = new THREE.MeshBasicMaterial({ color: 0x9900ff })
    let sphere = new THREE.Mesh(geo, material)
    return sphere
}

const grid = (min, max, spacing) => {
    let lines = []
    for(let i = min; i <= max; i += spacing) {
        for(let j = min; j <= max; j += spacing) {
            // let color = ( i == min && j == min ) ? 0x7F7FFF : 0xffffff;
            let color = 0xffffff
            let x = new THREE.Line(
                        new THREE.BufferGeometry()
                            .setFromPoints([new THREE.Vector3(j, i, min), new THREE.Vector3(j, i, max)]), 
                        new THREE.LineBasicMaterial({ color: color }));
            let y = new THREE.Line(
                        new THREE.BufferGeometry()
                            .setFromPoints([new THREE.Vector3(min, j, i), new THREE.Vector3(max, j, i)]), 
                        new THREE.LineBasicMaterial({ color: color }));
            let z = new THREE.Line(
                        new THREE.BufferGeometry()
                            .setFromPoints([new THREE.Vector3(i, min, j), new THREE.Vector3(i, max, j)]), 
                        new THREE.LineBasicMaterial({ color: color }));
            [x, y, z].forEach(e => { e.material.transparent = true; e.material.opacity = 0.4 })
            
            lines.push(x)
            lines.push(y)
            lines.push(z)
        }
    }

    return lines
}

const step = (scene) => {
    // window.sphere.position.x += 1
    for(let i in window.vectors) {
        if(window.nodes[i] == undefined) {
            window.nodes[i] = sphere()
            scene.add(window.nodes[i])
        }
        window.nodes[i].position.x = window.vectors[i][0] / 10
        window.nodes[i].position.y = window.vectors[i][1] / 10
        window.nodes[i].position.z = window.vectors[i][1] / 10
    }

}

const animate = (props) => () => {
    requestAnimationFrame( animate(props) )
    // render with three
    let { scene, camera, renderer } = props
    step(scene)
    renderer.render(scene, camera);
}

$(document).ready(() => {
    const { scene, camera, renderer } = initThree($(".three-handle"), $(".three-handle").width(), $(".three-handle").height())
    // setup
    camera.position.set(0, 0, -200)
    camera.lookAt(0, 0, 0)
    for(let i of grid(-100, 100, 50)) {
        scene.add(i)
    }
    window.sphere = sphere()
    // scene.add(window.sphere)
    animate({ scene, camera, renderer })()
})
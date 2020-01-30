p = {
    val: 1
}

function checkPointers(p) {
    setInterval(() => {
        console.log(p);
    }, 1000)
}

checkPointers(p)

setTimeout(() => { p.val = 2 }, 2000)
const WIDTH = 500;
const HEIGHT = 500;
const STROKE_WEIGHT = 3;
const drawingsContainer = document.querySelector(".drawings-container");

console.log(gameSocket);

gameSocket.onmessage = (e) => {
    console.log(`Server: ${e.data}`)
    const data = JSON.parse(e.data);
    const {payload} = data;
    if (payload.type === "draw") {
        const {
            canvas, x, y, px, py
        } = payload.data;
        const canvasElement = document.getElementById(canvas);
        const ctx = canvasElement.getContext("2d");
        ctx.beginPath();
        ctx.moveTo(px, py);
        ctx.lineTo(x, y);
        ctx.stroke();
    }
}

gameSocket.onopen = (e) => {
    console.log("Connected to websocket");
}

gameSocket.onclose = (e) => {
    console.log("Disconnected from websocket");
}

function setupCanvas(canvas, id) {
    console.log(connectionString);
    let timeout;
    let drawing = false;

    canvas.setup = () => {
        canvas.createCanvas(WIDTH, HEIGHT);
        canvas.strokeWeight(STROKE_WEIGHT);
        canvas.stroke("black");
        canvas.background("#FFFFFF");
        canvas.id = id;
        drawingsContainer.appendChild(canvas.canvas);
        canvas.canvas.id = id;
    }

    canvas.draw = () => {
        if (!drawing) return;
        canvas.line(canvas.mouseX, canvas.mouseY, canvas.pmouseX, canvas.pmouseY);
        gameSocket.send(JSON.stringify({
            type: "draw", data: {
                canvas: canvas.id, x: canvas.mouseX, y: canvas.mouseY, px: canvas.pmouseX, py: canvas.pmouseY
            }
        }));

        if (timeout) return;
        timeout = setTimeout(async () => {
            const image = canvas.canvas.toDataURL();
            const response = await fetch("/predict", {
                method: "POST", body: JSON.stringify({
                    image
                }), headers: {
                    "X-CSRFToken": csrftoken, "Content-Type": "application/json"
                }
            })
            const data = await response.text();
            console.log(data);
            timeout = null;
        }, 200);
    }

    canvas.mousePressed = () => drawing = canvas.mouseX > 0 && canvas.mouseX <= WIDTH && canvas.mouseY > 0 && canvas.mouseY <= HEIGHT;

    canvas.mouseReleased = () => drawing = false
}

new p5(leftCanvas => {
    setupCanvas(leftCanvas, "leftCanvas");
})

new p5(rightCanvas => {
    setupCanvas(rightCanvas, "rightCanvas");
})
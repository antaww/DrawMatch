const WIDTH = 500;
const HEIGHT = 500;
const STROKE_WEIGHT = 3;
const drawingsContainer = document.querySelector(".drawings-container");

function setupCanvas(canvas, id) {
    console.log(connectionString);
    const gameSocket = new WebSocket(connectionString);
    window.gameSocket = gameSocket;
    let timeout;
    let drawing = false;

    canvas.setup = () => {
        canvas.createCanvas(WIDTH, HEIGHT);
        canvas.strokeWeight(STROKE_WEIGHT);
        canvas.stroke("black");
        canvas.background("#FFFFFF");
        canvas.canvas.id = id;
        drawingsContainer.appendChild(canvas.canvas);

        gameSocket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            if (data.type === "draw") {
                const {
                    x, y, px, py
                } = data.data;
                canvas.line(x, y, px, py);
            }
        }

        gameSocket.addEventListener("close", (event) => {
            if (event.wasClean) {
                console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
            } else {
                console.log(`[close] Connection died, code=${event.code}, reason=${event.reason}`);
            }
        });

        gameSocket.addEventListener("error", event => {
            console.log(`Error occurred`);
            console.error(event)
        });

        gameSocket.addEventListener("open", ev => {
            console.log("Connected to websocket");
            console.log(ev)
        });
    }

    canvas.draw = () => {
        if (!drawing) return;
        canvas.line(canvas.mouseX, canvas.mouseY, canvas.pmouseX, canvas.pmouseY);

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
            gameSocket.send(JSON.stringify({
                type: "draw", data: {
                    x: canvas.mouseX, y: canvas.mouseY, px: canvas.pmouseX, py: canvas.pmouseY
                }
            }));
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
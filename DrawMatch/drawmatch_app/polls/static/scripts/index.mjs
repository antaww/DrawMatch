const WIDTH = 500;
const HEIGHT = 500;
const STROKE_WEIGHT = 3;
const drawingsContainer = document.querySelector(".drawings-container");

function setupCanvas(canvas, id) {
    canvas.setup = () => {
        canvas.createCanvas(WIDTH, HEIGHT);
        canvas.strokeWeight(STROKE_WEIGHT);
        canvas.stroke("black");
        canvas.background("#FFFFFF");
        canvas.canvas.id = id;
        drawingsContainer.appendChild(canvas.canvas);
    }

    canvas.draw = () => {
        if (canvas.mouseIsPressed && canvas.mouseX > 0 && canvas.mouseX <= WIDTH && canvas.mouseY > 0 && canvas.mouseY <= HEIGHT) {
            canvas.line(canvas.mouseX, canvas.mouseY, canvas.pmouseX, canvas.pmouseY);
            console.log(canvas.canvas.id);
        }
    }

    canvas.mouseReleased = async () => {
        //todo: send corresponding image to server, not both
        const image = canvas.canvas.toDataURL();
        console.log(image);
        const response = await fetch("/predict", {
            method: "POST",
            body: JSON.stringify({
                image
            }),
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            }
        })
        const data = await response.text();
        console.log(data);
    }
}

new p5(leftCanvas => {
    setupCanvas(leftCanvas, "leftCanvas");
})

new p5(rightCanvas => {
    setupCanvas(rightCanvas, "rightCanvas");
})

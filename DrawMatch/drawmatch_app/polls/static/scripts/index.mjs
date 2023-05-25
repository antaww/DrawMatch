const WIDTH = 500;
const HEIGHT = 500;
const STROKE_WEIGHT = 3;

new p5(p5 => {
    p5.setup = () => {
        p5.createCanvas(WIDTH, HEIGHT);
        p5.strokeWeight(STROKE_WEIGHT);
        p5.stroke("black");
        p5.background("#FFFFFF");
    }

    p5.draw = () => {
        if (p5.mouseIsPressed) {
            p5.line(p5.mouseX, p5.mouseY, p5.pmouseX, p5.pmouseY);
        }
    }

    p5.mouseReleased = async () => {
        const image = p5.canvas.toDataURL();
        const csrftoken = document.cookie.split(';').filter(c => c.trim().startsWith('csrftoken='))[0].split('=')[1];

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
})

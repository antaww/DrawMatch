const WIDTH = 500;
const HEIGHT = 500;
const STROKE_WEIGHT = 3;
const guesserDelay = 300; // ms
const storeDrawingDelay = 600; // ms
const drawingContainerLeft = document.querySelector(".drawing-container-left");
const drawingContainerRight = document.querySelector(".drawing-container-right");
const penSentence = document.querySelector(".pen-sentence");
const penPrediction = document.querySelector(".pen-prediction");
const array = [];
let isGameStarted = false;


// Send the array to the server every second to store the drawing
setInterval(async () => {
	if (array.length === 0) return;
	await fetch("/store-drawing", {
		method: "POST",
		body: JSON.stringify({
			array,
			room_code
		}),
		headers: {
			"X-CSRFToken": csrftoken,
			"Content-Type": "application/json"
		}
	});
	array.length = 0;
}, storeDrawingDelay);

gameSocket.onmessage = (e) => {
	const data = JSON.parse(e.data);
	const {payload} = data;
	if (payload.type === "draw") {
		const {
			canvas,
			x,
			y,
			px,
			py
		} = payload.data;
		const canvasElement = document.getElementById(canvas);
		const ctx = canvasElement.getContext("2d");
		ctx.beginPath();
		ctx.moveTo(px, py);
		ctx.lineTo(x, y);
		ctx.stroke();
	}
};

userJoinedSocket.onmessage = async e => {
	const data = JSON.parse(e.data);
	id_user_right = data.id_user_right;
	document.querySelector(".right-user-name").innerHTML = data.name_user_right;
	if (!isGameStarted) isGameStarted = true;

	const response = await fetch("/get-drawing", {
		method: "POST",
		body: JSON.stringify({
			room_code
		}),
		headers: {
			"X-CSRFToken": csrftoken,
			"Content-Type": "application/json"
		}
	});

	const drawings = await response.json();
	if (drawings.status === "not found") return;
	for (let i = 0; i < drawings.map.length; i++) {
		const drawing = drawings.map[i];
		const canvasElement = document.getElementById(drawing.canvas);
		const ctx = canvasElement.getContext("2d");
		ctx.beginPath();
		ctx.moveTo(drawing.px, drawing.py);
		ctx.lineTo(drawing.x, drawing.y);
		ctx.stroke();
	}
};

gameSocket.onopen = (e) => {
	console.log("Connected to websocket (game)");
};

gameSocket.onclose = (e) => {
	console.log("Disconnected from websocket (game)");
};

userJoinedSocket.onopen = (e) => {
	console.log("Connected to websocket (user joined)");
};

userJoinedSocket.onclose = (e) => {
	console.log("Disconnected from websocket (user joined)");
};

function setupCanvas(canvas, id) {
	let timeout;
	let drawing = false;

	canvas.setup = () => {
		canvas.createCanvas(WIDTH, HEIGHT);
		canvas.strokeWeight(STROKE_WEIGHT);
		canvas.stroke("black");
		canvas.background("#FFFFFF");
		canvas.id = id; // p5 id
		if (id === "leftCanvas") drawingContainerLeft.appendChild(canvas.canvas);
		if (id === "rightCanvas") drawingContainerRight.appendChild(canvas.canvas);
		canvas.canvas.id = id; // HTML id
	};

	canvas.draw = () => {
		if (!drawing) return;
		if (!isGameStarted) return;
		if (canvas.id === "leftCanvas" && id_user !== id_user_left) return;
		if (canvas.id === "rightCanvas" && id_user !== id_user_right) return;

		canvas.line(canvas.mouseX, canvas.mouseY, canvas.pmouseX, canvas.pmouseY);
		gameSocket.send(JSON.stringify({
			type: "draw",
			data: {
				canvas: canvas.id,
				x: canvas.mouseX,
				y: canvas.mouseY,
				px: canvas.pmouseX,
				py: canvas.pmouseY
			}
		}));

		const values = {
			canvas: canvas.id,
			x: canvas.mouseX,
			y: canvas.mouseY,
			px: canvas.pmouseX,
			py: canvas.pmouseY
		};
		array.push(values);

		if (timeout) return;
		timeout = setTimeout(async () => {
			const image = canvas.canvas.toDataURL();
			const response = await fetch("/predict", {
				method: "POST",
				body: JSON.stringify({
					image
				}),
				headers: {
					"X-CSRFToken": csrftoken,
					"Content-Type": "application/json"
				}
			});
			const data = await response.text();
			displayPrediction(data);
			timeout = null;
		}, guesserDelay);
	};

	canvas.mousePressed = () => drawing = canvas.mouseX > 0 && canvas.mouseX <= WIDTH && canvas.mouseY > 0 && canvas.mouseY <= HEIGHT;

	canvas.mouseReleased = () => drawing = false;
}

new p5(leftCanvas => {
	setupCanvas(leftCanvas, "leftCanvas");
});

new p5(rightCanvas => {
	setupCanvas(rightCanvas, "rightCanvas");
});

function displayPrediction(data) {
	const sentences = ["It's a", "Hmm a", "Oh, a", "I think it's a", "I'm pretty sure it's a"];
	let randomSentence = sentences[Math.floor(Math.random() * sentences.length)];
	const vowels = ["a", "e", "i", "o", "u"];

	// Correct the article if needed
	if (vowels.includes(data[0])) {
		randomSentence += "n";
		// Special case for "The ..."
	} else if (data.substring(0, 4) === "The ") {
		randomSentence = randomSentence.substring(0, randomSentence.length - 1);
	}

	penSentence.innerHTML = " " + randomSentence + " ";
	penPrediction.innerHTML = data;
}
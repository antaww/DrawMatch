import {displayError} from "./utils.mjs";

const WIDTH = 500;
const HEIGHT = 500;
const STROKE_WEIGHT = 3;
const guesserDelay = 300; // ms
const storeDrawingDelay = 600; // ms
const drawingContainerLeft = document.querySelector(".drawing-container-left");
const drawingContainerRight = document.querySelector(".drawing-container-right");
const penSentence = document.querySelector(".pen-sentence");
const penPrediction = document.querySelector(".pen-prediction");
const eraseButton = document.querySelector(".fa-trash-alt");
const wordToDraw = document.querySelector(".word-to-draw");
const leftScoreContainer = document.querySelector(".score-left");
const rightScoreContainer = document.querySelector(".score-right");
const leftUsername = document.querySelector(".left-user-name").innerHTML;
let rightUsername = "";
const drawingsDatas = [];
const wordsList = [];
let userLeftScore = 0;
let userRightScore = 0;
let isGameStarted = false;
let isGameEnded = false;


// Send the drawings datas to the server every storeDrawingDelay ms to store the drawing & avoid refresh loss
setInterval(async () => {
	if (drawingsDatas.length === 0) return;
	await fetch("/store-drawing", {
		method: "POST",
		body: JSON.stringify({
			drawingsDatas,
			room_code
		}),
		headers: {
			"X-CSRFToken": csrftoken,
			"Content-Type": "application/json"
		}
	});
	drawingsDatas.length = 0;
}, storeDrawingDelay);


// Drawings synchronisation
gameSocket.onmessage = async (e) => {
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
	} else if (payload.type === "erase") {
		const {canvas} = payload.data;
		const canvasElement = document.getElementById(canvas);
		const ctx = canvasElement.getContext("2d");
		ctx.beginPath();
		ctx.fillStyle = "#FFFFFF";
		ctx.fillRect(0, 0, WIDTH, HEIGHT);
		ctx.stroke();
	} else if (payload.type === "score") {
		await scoresManager();
	} else if (payload.type === "word") {
		const {
			word,
			username
		} = payload.data;

		displayError("Yes I know, it's " + word + " ! Well done " + username + " !", true);
		wordsList.length = 0;
		await getWordsFromServer();
	}
};


// User joined synchronisation
userJoinedSocket.onmessage = async e => {
	const data = JSON.parse(e.data);
	id_user_right = data.id_user_right;
	document.querySelector(".right-user-name").innerHTML = data.name_user_right;
	rightUsername = data.name_user_right;

	await scoresManager();

	if (userLeftScore + userRightScore >= 7) {
		endGame();
	}
	if (isGameEnded) return;

	if (!isGameStarted) {
		isGameStarted = true;
		await fetch("/generate-words", {
			method: "POST",
			body: JSON.stringify({
				room_code
			}),
			headers: {
				"X-CSRFToken": csrftoken,
				"Content-Type": "application/json"
			}
		});
	}

	await getWordsFromServer();

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

// DEBUG // todo: remove
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

// END DEBUG //


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
		if (isGameEnded) return;
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
		drawingsDatas.push(values);

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
			await checkPrediction(data, canvas.id);
			timeout = null;
		}, guesserDelay);
	};

	canvas.mousePressed = () => drawing = canvas.mouseX > 0 && canvas.mouseX <= WIDTH && canvas.mouseY > 0 && canvas.mouseY <= HEIGHT;

	canvas.mouseReleased = () => drawing = false;

	eraseButton.addEventListener("click", async () => {
		if (canvas.id === "leftCanvas" && id_user !== id_user_left) return;
		if (canvas.id === "rightCanvas" && id_user !== id_user_right) return;
		canvas.background("#FFFFFF");

		// Erase the drawing for the other user
		gameSocket.send(JSON.stringify({
			type: "erase",
			data: {
				canvas: canvas.id
			}
		}));

		// Erase the drawing from the server cache
		await fetch("/erase-drawing", {
			method: "POST",
			body: JSON.stringify({
				room_code,
				canvas: canvas.id
			}),
			headers: {
				"X-CSRFToken": csrftoken,
				"Content-Type": "application/json"
			}
		});
	});
}

new p5(leftCanvas => {
	if (isGameEnded) return;
	setupCanvas(leftCanvas, "leftCanvas");
});

new p5(rightCanvas => {
	if (isGameEnded) return;
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

async function getWordsFromServer() {
	const wordsResponse = await fetch("/get-words", {
		method: "POST",
		body: JSON.stringify({
			room_code
		}),
		headers: {
			"X-CSRFToken": csrftoken,
			"Content-Type": "application/json"
		}
	});
	const words = await wordsResponse.json();
	if (words.status !== "not found") {
		for (let i = 0; i < words.words.length; i++) {
			if (!wordsList.includes(words.words[i])) wordsList.push(words.words[i]);
		}
		console.log(wordsList); //todo: remove this
		if (wordsList.length > 0) {
			wordToDraw.innerHTML = wordsList[0];
		} else {
			endGame();
		}
	}
}

async function removeFirstWord() {
	await fetch("/remove-first-word", {
		method: "POST",
		body: JSON.stringify({
			room_code
		}),
		headers: {
			"X-CSRFToken": csrftoken,
			"Content-Type": "application/json"
		}
	});
}

async function checkPrediction(data, canvas) {
	if (data === wordsList[0]) {
		let username;
		username = canvas === "leftCanvas" ? leftUsername : rightUsername;

		//Add score to the user in server cache
		await fetch("/add-score", {
			method: "POST",
			body: JSON.stringify({
				room_code,
				position: canvas === "leftCanvas" ? "left" : "right",
				score: canvas === "leftCanvas" ? userLeftScore : userRightScore
			}),
			headers: {
				"X-CSRFToken": csrftoken,
				"Content-Type": "application/json"
			}
		});

		//Display the score
		gameSocket.send(JSON.stringify({
			type: "score",
			data: {
				room_code,
			}
		}));

		await removeFirstWord();

		gameSocket.send(JSON.stringify({
			type: "word",
			data: {
				room_code,
				word: data,
				username: username
			}
		}));
	}
}

function endGame() {
	isGameEnded = true;
	const canvases = document.querySelectorAll("canvas");
	wordToDraw.remove();
	canvases.forEach(canvas => canvas.remove());
	eraseButton.remove();

	const winner = userLeftScore > userRightScore ? leftUsername : rightUsername;
	const winnerId = winner === leftUsername ? id_user_left : id_user_right;
	//todo: add a win to the winner in the database

	// Pen voice
	penSentence.innerHTML = " Well played ";
	penPrediction.innerHTML = winner;

	// Display the winner
	const leftUsernameContainer = document.querySelector(".left-user-name");
	const rightUsernameContainer = document.querySelector(".right-user-name");
	leftUsernameContainer.innerHTML = leftUsername + (winner === leftUsername ? " won" : " lost");
	rightUsernameContainer.innerHTML = rightUsername + (winner === rightUsername ? " won" : " lost");
}

async function scoresManager() {
	const scoreResponse = await fetch("/get-scores", {
		method: "POST",
		body: JSON.stringify({
			room_code
		}),
		headers: {
			"X-CSRFToken": csrftoken,
			"Content-Type": "application/json"
		}
	});

	const score = await scoreResponse.json();
	if (score.status === "not found") {
		userLeftScore = 0;
		userRightScore = 0;
	} else {
		if (score.score.left !== undefined) userLeftScore = score.score.left;
		else userLeftScore = 0;

		if (score.score.right !== undefined) userRightScore = score.score.right;
		else userRightScore = 0;
	}

	leftScoreContainer.innerHTML = userLeftScore;
	rightScoreContainer.innerHTML = userRightScore;
}
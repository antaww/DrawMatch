import {displayError} from "./utils.mjs";

async function callServer(e, form, route) {
	e.preventDefault();

	const response = await fetch(route, {
		method: "POST",
		body: JSON.stringify({
			username: form.username.value,
			password: form.password.value
		}),
		headers: {
			"X-CSRFToken": csrftoken,
			"Content-Type": "application/json"
		}
	});

	const data = await response.text();
	if (response.status === 200) {
		window.location.href = "/";
	} else {
		displayError(data)
	}
}

document.addEventListener("DOMContentLoaded", () => {
	const loginForm = document.querySelector(".login-form");
	const loginBtn = document.querySelector("#login-btn");
	const registerBtn = document.querySelector("#register-btn");

	registerBtn.addEventListener("click", async (e) => {
		await callServer(e, loginForm, "/register-route");
	});

	loginBtn.addEventListener("click", async (e) => {
		await callServer(e, loginForm, "/login-route");
	});
});
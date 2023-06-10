async function callServer(e, form, route) {
    e.preventDefault();
    console.log(form.username.value, form.password.value);
    const response = await fetch(route, {
        method: "POST",
        body: JSON.stringify({
            username: form.username.value,
            password: form.password.value
        }), headers: {
            "X-CSRFToken": csrftoken, "Content-Type": "application/json"
        }
    });

    const data = await response.text();
    console.log(data);
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded");
    const loginForm = document.querySelector(".login-form");
    const loginBtn = document.querySelector("#login-btn");
    const registerBtn = document.querySelector("#register-btn");

    registerBtn.addEventListener("click", async (e) => {
        await callServer(e, loginForm, "/register");
    });

    loginBtn.addEventListener("click", async (e) => {
        await callServer(e, loginForm, "/login-route");
    });
});
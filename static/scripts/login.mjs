document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded");
    const loginForm = document.querySelector(".login-form");
    const loginBtn = document.querySelector("#login-btn");
    const registerBtn = document.querySelector("#register-btn");

    registerBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        console.log(loginForm.username.value, loginForm.password.value);
        const response = await fetch("/register", {
            method: "POST",
            body: JSON.stringify({
                username: loginForm.username.value,
                password: loginForm.password.value
            }), headers: {
                "X-CSRFToken": csrftoken, "Content-Type": "application/json"
            }
        });

        const data = await response.text();
        console.log(data);
    });
});
document.addEventListener('DOMContentLoaded', () => {
	const logoutBtn = document.querySelector('#logout-btn');

	logoutBtn.addEventListener('click', async () => {
		await fetch('/logout-route', {
			method: "POST",
			headers: {
				"X-CSRFToken": csrftoken
			}
		})

		window.location.href = "/";
	});
});
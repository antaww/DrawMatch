document.addEventListener('DOMContentLoaded', () => {
	const createRoomBtn = document.querySelector('#create-room-btn');

	createRoomBtn.addEventListener('click', async () => {
		const response = await fetch('/create-room-route', {
			method: "GET",
			headers: {
				"X-CSRFToken": csrftoken
			}
		});

		const data = await response.text();

		if (response.status === 200) {
			window.location.href = `/room/${data}`;
		} else {
			alert(data);
		}
	});
});
document.addEventListener('DOMContentLoaded', () => {
	const joinRoomForm = document.querySelector('.join-room-form');

	joinRoomForm.addEventListener('submit', (e) => {
		e.preventDefault();
		const formData = new FormData(joinRoomForm);
		const roomCode = formData.get('room-code');

		if (roomCode.length < 6) {
			joinRoomForm.classList.add('shake');
			return;
		}

		window.location.href = `/room/${roomCode}`;
	});

	joinRoomForm.addEventListener('animationend', () => {
		joinRoomForm.classList.remove('shake');
	});
});
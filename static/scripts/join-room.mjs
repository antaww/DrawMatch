document.addEventListener('DOMContentLoaded', () => {
	const joinRoomForm = document.querySelector('.join-room-form');

	joinRoomForm.addEventListener('submit', (e) => {
		e.preventDefault();
		const formData = new FormData(joinRoomForm);
		const roomCode = formData.get('room-code');

		window.location.href = `/room/${roomCode}`;
	});
});
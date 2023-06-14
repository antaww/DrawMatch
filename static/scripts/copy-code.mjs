document.addEventListener('DOMContentLoaded', () => {
	const roomCode = document.querySelector('.room-code');

	roomCode.addEventListener('click', () => {
		const roomCodeText = roomCode.innerText;
        alert(`Copy is not supported by HTTP protocol. Please copy the room code manually : ${roomCodeText}`);

        // Navigator.clipboard is not supported by HTTP protocol
		// navigator.clipboard.writeText(roomCodeText).then(r => {
		// 	alert('Copied to clipboard');
		// }).catch(err => {
		// 	alert('Failed to copy to clipboard');
		// });
	});
});
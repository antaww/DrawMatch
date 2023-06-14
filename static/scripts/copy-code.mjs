// import {displayError} from "./utils.mjs";

document.addEventListener('DOMContentLoaded', () => {
	const roomCode = document.querySelector('.room-code');

	roomCode.addEventListener('click', () => {
		const roomCodeText = roomCode.innerText;
        alert(`Copy is not supported by HTTP protocol. Please copy the room code manually : ${roomCodeText}`);

        // Navigator.clipboard is not supported by HTTP protocol
		// navigator.clipboard.writeText(roomCodeText).then(r => {
		// 	displayError('Copied to clipboard')
		// }).catch(err => {
		// 	displayError('Failed to copy to clipboard')
		// });
	});
});
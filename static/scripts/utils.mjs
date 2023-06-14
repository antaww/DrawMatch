export function displayError(data) {
	let notice = document.createElement("span");
	notice.className = "notice visible";
	notice.innerHTML = data;
	document.body.appendChild(notice);
	setTimeout(() => {
		document.body.removeChild(notice);
	}, 3000);
}
export function displayError(data, announce = false) {
	let notice = document.createElement("span");
	notice.className = "notice visible";
	if (announce) {
		notice.className += " announce";
	}
	notice.innerHTML = data;
	document.body.appendChild(notice);
	setTimeout(() => {
		document.body.removeChild(notice);
	}, 6000);
}
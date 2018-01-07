/**
 * Created by phil on 25/12/2016.
 */

function saveParams() {
	if (document.getElementById("server").value) {
		localStorage.setItem("server", document.getElementById("server").value);
		localStorage.setItem("user", document.getElementById("user").value);
		localStorage.setItem("pass", document.getElementById("pass").value);
		window.location.href = "main.html";
	}
	else {
		alert("The server field is required.");
	}
}

function readServer() {
	return localStorage.getItem("server");
}

function readUser() {
	if (localStorage.getItem("user")) {
		return localStorage.getItem("user");
	}
	else {
		return undefined;
	}

}

function readPass() {
	if (localStorage.getItem("pass")) {
		return localStorage.getItem("pass");
	}
	else {
		return undefined;
	}
}

function clearParams() {
	localStorage.removeItem("server");
	localStorage.removeItem("user");
	localStorage.removeItem("pass");
}

function resetApp() {
	if (confirm("This will clear the client settings, and then close the window.\n\nProceed?")) {
		clearParams();
		window.close();
	}
}

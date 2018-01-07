/**
 * Created by phil on 05/03/2017.
 */

var ws = new WebSocket("ws://" + readServer() + ":8080/");
var pcap_b64 = "";
var pcap_blob;
var pcap_filename;
var rules_batch_file = "";
var rules_batch_blob;
var i = 0;

ws.onopen = function () {
	ws.send("auth");
	console.log(readUser());
	console.log(readPass());
	ws.send(readUser());
	ws.send(readPass());
	changePane("home", "home_nav");
	resetFooterStatus();
};
ws.onclose = function () {
	alert("Connection closed.");
	document.getElementById("footer-status").innerHTML = "Disconnected. Ctrl/Cmd + R to reconnect.";
};
ws.onmessage = function (event) {
	console.log("MESSAGE: " + event.data);
	if (event.data == "ok") {
		console.log("Credentials accepted");
	}
	else if (event.data == "bad") {
		alert("The credentials entered were invalid.");
	}
	else {
		switch (getState()) {
			case "home":
				var stats = event.data.split(" ");
				document.getElementById("analysedNum").innerHTML = stats[0];
				document.getElementById("processingNum").innerHTML = stats[1];
				document.getElementById("waitingNum").innerHTML = stats[2];
				break;
			case "active":
				var jobs = JSON.parse(event.data);
				if (jobs.length > 0) {
					var table_data = "";
					for (i = 0; i < jobs.length; i++) {
						table_data += ('<tr onclick="changePane(\'job-overview\', \'job_nav\', \'' + jobs[i]._id + '\')">');
						table_data += ('<td>' + jobs[i]._id + '</td>');
						table_data += ('<td>' + jobs[i].filename + '</td>');
						table_data += ('<td>' + jobs[i].machine + '</td>');
						table_data += ('<td>' + jobs[i].date_time + '</td></tr>');
					}
					document.getElementById("active-body").innerHTML = table_data;
					document.getElementById("active-nothing").classList.add("hidden");
					document.getElementById("active-nothing").classList.remove("shown");
				}
				else {
					document.getElementById("active-body").innerHTML = "";
					document.getElementById("active-nothing").classList.add("shown");
					document.getElementById("active-nothing").classList.remove("hidden");
				}
				break;
			case "waiting":
				var jobs = JSON.parse(event.data);
				if (jobs.length > 0) {
					var table_data = "";
					for (i = 0; i < jobs.length; i++) {
						table_data += ('<tr onclick="changePane(\'job-overview\', \'job_nav\', \'' + jobs[i]._id + '\')">');
						table_data += ('<td>' + jobs[i]._id + '</td>');
						table_data += ('<td>' + jobs[i].filename + '</td>');
						table_data += ('<td>' + jobs[i].machine + '</td>');
						table_data += ('<td>' + jobs[i].date_time + '</td></tr>');
					}
					document.getElementById("waiting-body").innerHTML = table_data;
					document.getElementById("waiting-nothing").classList.add("hidden");
					document.getElementById("waiting-nothing").classList.remove("shown");
				}
				else {
					document.getElementById("waiting-body").innerHTML = "";
					document.getElementById("waiting-nothing").classList.add("shown");
					document.getElementById("waiting-nothing").classList.remove("hidden");
				}
				break;
			case "jobs":
				var jobs = JSON.parse(event.data);
				if (jobs.length > 0) {
					var table_data = "";
					for (i = 0; i < jobs.length; i++) {
						table_data += ('<tr onclick="changePane(\'job-overview\', \'job_nav\', \'' + jobs[i]._id + '\')">');
						table_data += ('<td>' + jobs[i]._id + '</td>');
						table_data += ('<td>' + jobs[i].filename + '</td>');
						table_data += ('<td>' + jobs[i].machine + '</td>');
						table_data += ('<td>' + jobs[i].date_time + '</td></tr>');
					}
					document.getElementById("jobs-body").innerHTML = table_data;
					document.getElementById("jobs-nothing").classList.add("hidden");
					document.getElementById("jobs-nothing").classList.remove("shown");
				}
				else {
					document.getElementById("jobs-body").innerHTML = "";
					document.getElementById("jobs-nothing").classList.add("shown");
					document.getElementById("jobs-nothing").classList.remove("hidden");
				}
				break;
			case "job-overview":
				var job = JSON.parse(event.data);
				document.getElementById("statusHero").innerHTML = job.status.toUpperCase();
				if (job.status.toUpperCase() != "FINISHED") {
					document.getElementById("networkNum").innerHTML = "-";
					document.getElementById("rulesButton").disabled = true;
					document.getElementById("pcapButton").disabled = true;
				}
				else {
					if (job.addresses == null) {
						document.getElementById("networkNum").innerHTML = "0";
					}
					else {
						document.getElementById("networkNum").innerHTML = job.addresses.length;
					}
					document.getElementById("rulesButton").disabled = false;
					document.getElementById("pcapButton").disabled = false;
				}
				document.getElementById("runtimeNum").innerHTML = job.duration + "s";
				var table_data = "";
				table_data += "<tr><td>ID</td><td>" + job._id + "</td></tr>";
				table_data += "<tr><td>Filename</td><td class='selectable-text'>" + job.filename + "</td></tr>";
				table_data += "<tr><td>Machine</td><td>" + job.machine + "</td></tr>";
				table_data += "<tr><td>Added</td><td>" + job.date_time + "</td></tr>";
				if (job.status.toUpperCase() == "WAITING") {
					table_data += "<tr><td>MD5</td><td class='hash selectable-text'>" + "-" + "</td></tr>";
				}
				else {
					table_data += "<tr><td>MD5</td><td class='hash selectable-text'>" + job.md5 + "</td></tr>";
				}

				document.getElementById("overview-body").innerHTML = table_data;
				break;
			case "job-network":
				var job = JSON.parse(event.data);
				var table_data = "";
				if (job.addresses == null) {
					document.getElementById("addressNum").innerHTML = "0";
					document.getElementById("network-nothing").classList.add("shown");
					document.getElementById("network-nothing").classList.remove("hidden");
				}
				else {
					document.getElementById("addressNum").innerHTML = job.addresses.length;
					for (i = 0; i < job.addresses.length; i++) {
						table_data += ("<tr><td class='selectable-text'>" + job.addresses[i] + "</td></tr>");
					}
					document.getElementById("network-nothing").classList.add("hidden");
					document.getElementById("network-nothing").classList.remove("shown");
				}
				document.getElementById("network-body").innerHTML = table_data;

				break;
			case "upload":
				var stats = event.data.split(" ");
				document.getElementById("analysedHero").innerHTML = stats[0];
				document.getElementById("processingHero").innerHTML = stats[1];
				document.getElementById("waitingHero").innerHTML = stats[2];
				var options = "";
				for (i = 3; i < stats.length; i++) {
					options += ("<option value=\"" + stats[i] + "\">" + stats[i] + "</option>");
				}
				document.getElementById("vm-select").innerHTML = options;
				break;
			case "pcap":
				console.log("case: pcap");
				document.getElementById("footer-status").innerHTML = "Downloading PCAP: ";
				i = 0;
				if (event.data != "finished.") {
					i++;
					pcap_b64 += event.data;
					document.getElementById("footer-status").innerHTML = "Downloading PCAP: " + (i * 130000) + " bytes";
				}
				else {
					document.getElementById("footer-status").innerHTML = "Download complete";
					pcap_blob = b64toBlob(pcap_b64, "application/cap");
					pcap_filename = getCurrentJob() + ".pcap";
					download(pcap_blob, pcap_filename);
					// Hate this, but otherwise subsequent downloads fail due to weird page caching
					setTimeout(refresh(), 500);
				}
				break;
			case "rules":
				var job = JSON.parse(event.data);
				if (job.addresses == null) {
					alert("There aren't any addresses to create firewall rules with!");
				}
				else {
					// Batch file lines to setup, and prompt user if they wish to continue
					rules_batch_file = "@echo off\nsetlocal\n:PROMPT\nSET /P AREYOUSURE=Running this will 'ping' each" +
						" of the addresses to resolve their IPs. Are you sure you want to continue? (y/n): \n" +
						"IF /I \"%AREYOUSURE%\" NEQ \"y\" GOTO END\n";
					for (i = 0; i < job.addresses.length; i++) {
						rules_batch_file += "echo Pinging " + job.addresses[i] + " to resolve IP...\n";
						// Batch file line to resolve the IP address
						rules_batch_file += "for /f \"tokens=1,2 delims=[]\" %%A in ('ping " + job.addresses[i] +
							" -n 1 ^| find \"Pinging\"') do set ipaddress=%%B\n";
						rules_batch_file += "echo " + job.addresses[i] + " resolved to %ipaddress%\n";
						// Tell user which IP is being added
						rules_batch_file += "echo Adding %ipaddress% to firewall list\n";
						// Create firewall rule
						rules_batch_file += "netsh advfirewall firewall add rule name=\"" + getCurrentJob() + "-" + i +
							"\" dir=out action=block enable=yes remoteip=%ipaddress%\n";
					}
					// End file
					rules_batch_file += ":END\nendlocal\npause\n";
					rules_batch_blob = new Blob([rules_batch_file], {type: "application/bat"});
					download(rules_batch_blob, getCurrentJob() + "-rules.bat");
					setTimeout(refresh(), 500);
				}
		}
	}
};

function sendRequest(state) {
	ws.send(state);
}

function uploadSample() {
	if (document.getElementById("sample-file").value && document.getElementById("vm-select").value
		&& document.getElementById("run-time").value) {
		document.getElementsByTagName("body")[0].classList.add("busy");
		var filereader = new FileReader();
		var sample = document.getElementById("sample-file").files[0];

		sendRequest("file");
		sendRequest(document.getElementById("sample-file").files[0].name);
		console.log(document.getElementById("sample-file").files[0].name);
		sendRequest(document.getElementById("vm-select").value);
		sendRequest(document.getElementById("run-time").value);

		document.getElementById("footer-status").innerHTML = "Uploading: ";

		filereader.addEventListener("load", function () {
			// websocketd has a character limit for messages, so split file into multiple messages
			for (i = 0; i < filereader.result.length % 130000; i++) {
				sendRequest(filereader.result.substring((i * 130000), (i * 130000) + 130000));
				document.getElementById("footer-status").innerHTML = "Uploading: " + (i * 130000) + " bytes";
			}
			sendRequest("file_done");
			document.getElementById("footer-status").innerHTML = "Upload complete";
			document.getElementsByTagName("body")[0].classList.remove("busy");
			setTimeout(changePane("home", "home_nav"), 1000);
			setTimeout(refresh(), 1200);
		}, false);

		filereader.readAsDataURL(sample);
	}
	else {
		alert("One or more fields are missing data.");
	}
}

function b64toBlob(b64Data, contentType) {
	var sliceSize = 512;
	var byteCharacters = atob(b64Data);
	var byteArrays = [];

	for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
		var slice = byteCharacters.slice(offset, offset + sliceSize);
		var byteNumbers = new Array(slice.length);

		for (i = 0; i < slice.length; i++) {
			byteNumbers[i] = slice.charCodeAt(i);
		}

		var byteArray = new Uint8Array(byteNumbers);
		byteArrays.push(byteArray);
	}

	var blob = new Blob(byteArrays, {type: contentType});
	return blob;
}

function download(file, filename) {
	var a = document.createElement("a");
	var url = URL.createObjectURL(file);

	a.href = url;
	a.download = filename;
	document.body.appendChild(a);
	a.click();

	setTimeout(function() {
		document.body.removeChild(a);
		window.URL.revokeObjectURL(url);
	}, 0);
}

function resetFooterStatus() {
	switch (ws.readyState) {
		case ws.CONNECTING:
			document.getElementById("footer-status").innerHTML = "Connecting to " + readServer();
			break;
		case ws.OPEN:
			document.getElementById("footer-status").innerHTML = "Connected to " + readServer();
			break;
		case ws.CLOSING:
			document.getElementById("footer-status").innerHTML = "Connection closing...";
			break;
		case ws.CLOSED:
			document.getElementById("footer-status").innerHTML = "Disconnected. Ctrl/Cmd + R to reconnect.";
			break;
		default:
			document.getElementById("footer-status").innerHTML = "Unknown connection state";
			break;
	}
}

/**
 * Created by phil on 26/12/2016.
 */

var state;
var currentJob;

function changePane(target, targetNav, jobID) {
	state = target;

    // Hide all frames first (and deactivate all nav bar rows)
    document.getElementById("home").classList.remove("shown");
    document.getElementById("home").classList.add("hidden");
    document.getElementById("home_nav").classList.remove("active");
    document.getElementById("active").classList.remove("shown");
    document.getElementById("active").classList.add("hidden");
    document.getElementById("active_nav").classList.remove("active");
    document.getElementById("waiting").classList.remove("shown");
    document.getElementById("waiting").classList.add("hidden");
    document.getElementById("waiting_nav").classList.remove("active");
    document.getElementById("upload").classList.remove("shown");
    document.getElementById("upload").classList.add("hidden");
    document.getElementById("jobs").classList.remove("shown");
    document.getElementById("jobs").classList.add("hidden");
    document.getElementById("jobs_nav").classList.remove("active");
    document.getElementById("job-overview").classList.remove("shown");
    document.getElementById("job-overview").classList.add("hidden");
    document.getElementById("job_nav").classList.remove("active");
    document.getElementById("job-network").classList.remove("shown");
    document.getElementById("job-network").classList.add("hidden");
    document.getElementById("network_nav").classList.remove("active");

    // Then show the requested one
    document.getElementById(target).classList.remove("hidden");
    document.getElementById(target).classList.add("shown");

    // Handle special cases
    if (target !== "upload") {
	    document.getElementById(targetNav).classList.add("active");
    }
    if (target.substring(0, 4) === "job-") {
        document.getElementById("job_nav_group").classList.remove("hidden");
        document.getElementById("job_nav_group").classList.add("shown");
    }
    else {
        document.getElementById("job_nav_group").classList.add("hidden");
        document.getElementById("job_nav_group").classList.remove("shown");
    }

    // Show the extra buttons when needed
    if (target === "job-network") {
        document.getElementById("rulesButton").classList.remove("hidden");
        document.getElementById("rulesButton").classList.add("shown");
        document.getElementById("pcapButton").classList.remove("hidden");
        document.getElementById("pcapButton").classList.add("shown");
    }
    else {
        document.getElementById("rulesButton").classList.add("hidden");
        document.getElementById("rulesButton").classList.remove("shown");
        document.getElementById("pcapButton").classList.add("hidden");
        document.getElementById("pcapButton").classList.remove("shown");
    }

    if (target.substring(0, 4) === "job-") {
    	if (jobID !== undefined) {
    		currentJob = jobID;
	    }
    	sendRequest("details");
    	sendRequest(currentJob);
    }
    else {
    	sendRequest(target);
    }

    resetFooterStatus();
}

function getState() {
	return state;
}

function getCurrentJob() {
    return currentJob;
}

function btnPCAP() {
    state = "pcap";
    sendRequest("pcap");
    sendRequest(currentJob);
}

function btnRules() {
    state = "rules";
    sendRequest("details");
    sendRequest(currentJob);
}

function refresh() {
	location.reload();
}

/**
 * Created by phil on 25/12/2016.
 */

document.addEventListener('DOMContentLoaded', function () {
	var splash = document.getElementsByClassName('shown')[0];
	var form = document.getElementsByClassName('hidden')[0];
	var button = document.getElementById("begin");

	button.addEventListener('click', function () {
		if (splash.classList.contains('hidden')) {
			// show
			splash.classList.add('transition');
			splash.clientWidth; // force layout to ensure the now display: block and opacity: 0 values are taken into account when the CSS transition starts.
			splash.classList.remove('hidden');
		} else {
			// hide
			splash.classList.add('transition');
			splash.classList.add('hidden');
		}
		if (form.classList.contains('hidden')) {
			// show
			form.classList.add('transition');
			form.clientWidth; // force layout to ensure the now display: block and opacity: 0 values are taken into account when the CSS transition starts.
			form.classList.remove('hidden');
		} else {
			// hide
			form.classList.add('transition');
			form.classList.add('hidden');
		}
	}, false);

	splash.addEventListener('transitionend', function () {
		splash.classList.remove('transition');
	}, false);

	form.addEventListener('transitionend', function () {
		form.classList.remove('transition');
		document.getElementsByClassName("form-title")[0].classList.add("fadeIn");
		setTimeout(function () {
			document.getElementsByClassName("form-content")[0].classList.add("fadeIn");
		}, 650);
		setTimeout(function () {
			document.getElementById("setup-form").classList.add("fadeIn");
		}, 1100);
	}, false);
});

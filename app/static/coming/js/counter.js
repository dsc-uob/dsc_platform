const daysElement = document.querySelector("#days");
const hoursElement = document.querySelector("#hours");
const minsElement = document.querySelector("#mins");
const secsElement = document.querySelector("#secs");

// Set the date we're counting down to
let countDownDate = new Date("Dec 1, 2020 00:00:00").getTime();

// Update the count down every 1 second
let x = setInterval(function () {

	// Get today's date and time
	let now = new Date().getTime();

	// Find the distance between now and the count down date
	let distance = countDownDate - now;

	// Time calculations for days, hours, minutes and seconds
	let days = Math.floor(distance / (1000 * 60 * 60 * 24));
	let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	let seconds = Math.floor((distance % (1000 * 60)) / 1000);

	daysElement.innerHTML = `${days} <sup>days</sup>`;
	hoursElement.innerHTML = `${hours} <sup>hours</sup>`;
	minsElement.innerHTML = `${minutes} <sup>mins</sup>`;
	secsElement.innerHTML = `${seconds} <sup>secs</sup>`;
}, 1000);
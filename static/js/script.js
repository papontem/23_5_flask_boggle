$(document).ready(function () {
	console.log("html is ready");
	console.log("URL href:", window.location.href);
});

// const BASE_URL = "127.0.0.1:5000";

function update_dom_highscore(highscore){
	console.log("updating dom highscore");
	let current_highscore = +$("#highscore").text()
	if (current_highscore < highscore){
		$("#highscore").text(highscore)
	}
}

async function update_highscore_server(){
	/**
	 * function to update the highscore saved in server by axios post request. 
	 */
	console.log("update_highscore_server");
	// pam: creatinga payload variable for easier editing
	let payload = { "score": $("#score").text() };

	try {
        // for some reason, my flask server is not getting the payload...fixed was sending info as json not as args or form 
		const response = await axios({
			url: "http://127.0.0.1:5000/score_update",
			method: "POST",
			data: payload,
		});
        // following are for debugging
		console.log("Response:", response);
		console.log("Response Data:", response.data);
		console.log("Response Data highscore:", response.data["highscore"]);

		// now update the doms highscore
		update_dom_highscore(response.data["highscore"])

	} catch (error) {
		console.error("ERROR!");
		console.error("Error message:", error.message);
		console.error("Error status:", error.response.status);
		console.error("Error headers:", error.response.headers);
		console.error("Error data:", error.response.data);
	}
}
function update_score(guess,result){
	/**
	 * function to update the dom score element 
	 */
	console.log("update_score")
	// console.log("guess:", guess);
	// console.log("result:",result);

	// update the score dom element if word was accepted, dont wanna increase score if user entered invalid input
	if (result == "ok") {
		// get score inner text string value and turn it into an int with a plus sign
		let score_value =  +$("#score").text();
		// increase score by length of the guess
		score_value += guess.length
		// change score using jquerry ezpz
		$("#score").text(score_value)
		// console.log("Your Score:", score_value);
		update_highscore_server()
	}
}

function update_guess_list(guess,result){
	console.log("update_guess_list")
    // cconsole.log("guess:", guess);
    // console.log("result:",result);
	
    // Create the new li element
    let new_li = $(`<li class=${result}>`).text(`${guess.toUpperCase()} : ${result}`);

    // Append the new li element to the guesses list
    $('#guesses').append(new_li);
}

// pam: add even listener to any form with our guess-word-form id
$("#guess-word-form").on("submit", async function (event) {
	event.preventDefault();

	// pam: get the word the user is guessing from the froms input input
	let guessInputValue = $("#guess").val();
	console.log("guessInputValue:", guessInputValue);
	$("#guess").val("")
	// pam: creatinga payload variable for easier editing
	let payload = { "guess": guessInputValue };

	// pam: make axios api post request
	// pam: TODO currently causing an axios status error of 500, and a flask server error of 500 then 400 for a BadRequestKeyError: FIXED
	try {
        // for some reason, my flask server is not getting the payload...fixed was sending info as json not as args or form 
		const response = await axios({
			url: "http://127.0.0.1:5000/guess",
			method: "POST",
			data: payload,
		});
        // following are for debugging
		console.log("Response:", response);
		console.log("Response Data:", response.data);
		console.log("Response Data Result:", response.data["result"]);

        // update the dom elements
        update_guess_list(guessInputValue,response.data["result"])
		update_score(guessInputValue,response.data["result"])

	} catch (error) {
		console.error("ERROR!");
		console.error("Error message:", error.message);
		console.error("Error status:", error.response.status);
		console.error("Error headers:", error.response.headers);
		console.error("Error data:", error.response.data);
	}

});

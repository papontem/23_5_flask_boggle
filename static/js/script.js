$(document).ready(function () {
	console.log("html is ready");
	console.log("URL href:", window.location.href);
});

// const BASE_URL = "127.0.0.1:5000";

function update_guess_list(guess,result){
    console.log(guess);
    console.log(result);

    // Create the new li element
    let new_li = $('<li>').text(`${guess} : ${result}`);

    // Append the new li element to the guesses list
    $('#guesses').append(new_li);
}

// pam: add even listener to any form with our guess-word-form id
$("#guess-word-form").on("submit", async function (event) {
	event.preventDefault();

	// pam: get the word the user is guessing from the froms input input
	let guessInputValue = $("#guess").val();
	console.log("guessInputValue:", guessInputValue);

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

	} catch (error) {
		console.error("ERROR!");
		console.error("Error message:", error.message);
		console.error("Error status:", error.response.status);
		console.error("Error headers:", error.response.headers);
		console.error("Error data:", error.response.data);
	}

});

# Exercise 23.5 Flask Testing Boggle Web Game App

This repository contains a Python Flask web application that implements the classic game of Boggle. 

# Installation, Usage, and Testing

## Installation
To run the Boggle game web application locally, follow these steps:

1. Clone this repository to your local machine.
2. Make sure you have Python3.7 then install Flask 1.X and the rest of the requirements.txt with use of the command:
    -       pip install -r requirements.txt
3. Navigate to the project directory in your terminal.
4. Start the Flask development server run the command:
    -       flask run
5. Open a web browser and access the URL provided by the Flask server.

If you encounter any issues or have suggestions for improvements, please feel free to hit me up or open an issue in this repository.

Have fun playing Boggle!

## Usage: How to Play The Game

The goal of the game is to create words from a random assortment of letters in a 5x5 grid and earn the highest point total.

1. Once you access the web application through the local URL provided  by the flask server you will be shown the home page.
2. Press the Start Boogle game button at the at the center of the pages bottom to start the boggle game. 
3. The Boggle Game Board will be displayed, consisting of a 5x5 grid of randomly selected uppercase letters.
4. You will start of with a score of 0, your previously recorded highscore, a timer of 60 seconds (currently), and a empty list of guesses after the page finishes loading.
5. To create a word, you must link letters in sequence. Letters must be adjacent to each other horizontally, vertically, or diagonally.
6. To start guessing words just head to the guess a word input box right at the bottom of the board. Click the input box and start typing away. 
7. Once you have created a word, just press enter or click the "is it valid?" button to send the word you wrote for validation.
8. The application will validate the word, calculate the points earned, update the score live and put the word you guessed into the guess list right below the input box.
    - if the word sent does not exist in the current dictionary its marked as not a word and displayed with a red background.
    - if the word exists but is not found in any linked sequence inside the boggle board it is marked not on board and shown with a yellow background.
    - if its an existing word and is found inside our boggle board its marked ok and displayed with a green background.
9. Repeat steps 5-7 to create more words within the time limit.
10. The game ends when the time runs out, and the final score is displayed, along with your highscore for comparison the entire time the game is running.

## Features and Functionality

I was provided a starting boggle.py and words.txt file to build the rest of the web app from. The py file is the one that creates the raw data structure needed for me to dispplay a random boggle board with my html by flask+jinja templating, and the validation of words by reading the words.txt. Most of all I did was UI, server functionality and unit-testing. 

## What did I add?
- #### app.py
    - all routes
- #### test_app.py
    - tests for all routes
- #### static folder files
    - css
    - js
- #### template folder files
    - base.html
    - home.html
    - board.html

## Testing
To begin testing of this flask app:

1. Complete installation steps 1-3
2. in your terminal to run all tests input the unitest module command:
    -       python -m unittest
3. you should be able to see if anything goes wrong, but if the messeges arent enought you can go into the test_app.py code and place this snippet to diagnose the bug with pythons native debugger:
    -       import pdb
            pdb.set_trace()

## My To-Do List:

The following is a list of ideas for future improvements and features:

- [ ] Dont allow users to input words less than 2 letters long.
- [ ] Dont allow users to input duplicate words they've already tried guessing.
- [ ] Allow the the setting of custom time llimits, not just 60 seconds.
- [ ] Add a feature or restart button to randomize the letters on the board without leaving the game board page.
- [ ] Allow the creation of Boggle boards with custom dimensions, not just 5x5.
- [ ] Add a leaderboard functionality to track and display high scores.
- [ ] Implement a hint or suggestion system to assist players in finding words.
- [ ] Improve the user interface and styling to make the application more visually appealing.
- [ ] Enhance the mobile responsiveness of the application for a better experience on mobile devices.

Feel free to contribute to this project by tackling any of the items on the to-do list or adding your own ideas!



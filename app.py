from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension


"""
Step#1 
+looking at app.py no flask code was given, we will insert our own. 
This is where your routing logic should go.
PAM: understood Will do!


Step#2: Displaying the Board
+ Display the board in a Jinja template.
       - You will be generating a board on the backend using a function from the boggle.py file and sending that to your Jinja template.
       - Using Jinja, display the board on the page.
+ make sure to save the board in the flask session.
+ Once you have displayed the board, add a form that allows a user to submit a guess.
PAM: DONE

step#3:Checking for a Valid Word WITH AJAX!! 

"""


#flask requiered app name
app = Flask(__name__)

#flask debugtoolbar settings
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app) 


boggle_game = Boggle()

#GET
@app.route('/') #decorator expecting a function
def homepage(): #the function that will be executed when decorator is flagged
    """Show homepage"""


    # Keep a count of how many times page is visited
    session['visit_count'] = session.get('visit_count', 0) + 1
    # if its the users first time give them a thanks 
    if session['visit_count'] == 1:
        flash('Hi Im Phedias, I hope you enjoy this game. Thanks for taking a look.')

    return render_template("home.html")

@app.route('/start-game')
def start_game():
    """ initialize game board for this session and redirect user to generated board page"""
    
    board = boggle_game.make_board()

    session['board'] = board
    session['guess_list'] = []

    return redirect('/game-board')

@app.route('/game-board')
def show_board():
    """Show the user the boggle board"""
    # if theres no board in session show default for testing
    board = session.get('board',[
                    ['H', 'T', '+', '+','+'],
                    ['O', 'E', 'E', '+','+'],
                    ['M', '+', 'L', 'S','+'],
                    ['G', 'O', '+', 'L','T'],
                    ['K', 'C', 'A', 'B','O'],
                ])
    session['board'] = board

    return render_template("board.html", board=board)

@app.route('/guess' , methods=["POST", "GET"])
def validate_guess_word():
    """ here we will validate the guess of the word we were sent then return some json depending on the state of the validation """

    # none of these were working because axios sends data as json and not in flasks request.args or request.form dictionaries.
    # guess = request.form.get("guess_word", "FORM")
    # guess = request.args.get("guess_word", "ARGS")
    
    # this is to get the json from our request sent by axios, we set silent equal to true so that this method will fail silently and return None.
    payload = request.get_json(silent=True)
    if payload:
        guess_word = payload["guess"]
        board = session['board']

        # # Validation call
        result = boggle_game.check_valid_word(board, guess_word)
    else:
        result = "testing"

    # setting up return with some ifs 
    if result == "ok":
        result = {"result": "ok"}
        # update the guess list
        guess_list = session["guess_list"]
        guess_list.append(guess_word)
        session["guess_list"] = guess_list

    elif result == "not-on-board":
        result = {"result": "not-on-board"}
    # bobble.py is returning "not-word" when your guess_word is not a word
    elif result == "not-word":
        result = {"result": "not-a-word"}
    elif result == "testing":
        result ={"result": result}
    # import pdb
    # pdb.set_trace()
    # return the result of validation as json
    return jsonify(result)
from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
import sys

"""
Welcome to my FLask Boggle Web App.

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
    # time limit is in seconds e.i. value of 60 is same as 60 seconds
    session['time_limit'] = 60
    # check if user already has a highscore saved in our session for flask
    if 'highscore' not in session:
        session["highscore"] = 0
    
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
    """ 
    this function validates the guess of the word we were sent then returns a json payload with the result
    TODO: need to berify that usr hasnt inputed the same word twice, to prevent duplicates. 
    
    """

    # none of these were working because axios was sending data as json and not in flasks request.args or request.form dictionaries.
    # guess = request.form.get("guess_word", "FORM")
    # guess = request.args.get("guess_word", "ARGS")
    
    # this is to get the json from our request sent by axios, we set silent equal to true so that
    #  incase this method fails, it does so silently, without stopping logic and return None instead.
    payload = request.get_json(silent=True)

    if payload == None:
        result ={"result": "testing"}
        return jsonify(result)
    else:
        guess_word = payload["guess"]
        board = session['board']

        # # Validation call
        result = boggle_game.check_valid_word(board, guess_word)
        

    # setting up return with some ifs 
    if result == "ok":
        result = {"result": "ok"}
        # update the guess list
        guess_list = session["guess_list"]
        guess_list.append(guess_word)
        session["guess_list"] = guess_list

    if result == "not-on-board":
        result = {"result": "not-on-board"}
    # bobble.py is returning "not-word" when your guess_word is not a word
    if result == "not-word":
        result = {"result": "not-a-word"}
    
    # return the result of validation as json
    return jsonify(result)

@app.route('/score_update', methods=["POST"])
def update_tracked_user_score():
    """
    Takes score sent by axios js post request, compares to highscore saved in session, 
    if higher reassigns it
    returns some json with the new highscore
    """
    
    # added this for our unittest 
    if "highscore" not in session:
        session["highscore"] = 0
    

    payload = request.get_json(silent=True)
    # print("UPDATE HIGHSCORE ROUTE-> PAYLOAD RECIEVED: ", payload)
    # import pdb
    # pdb.set_trace()
    try:
        highscore = int(payload["score"])
        # print("highscore = ", highscore)
        
        if session["highscore"] < highscore:
            session["highscore"] = highscore
        
        result = {"highscore" : highscore}
        return jsonify(result)

    except: 
        # debuggin for ANY execption at all
        print("Exception error has occured in /score-update route")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("An exception occurred:")
        print("Type:", exc_type)
        print("Value:", exc_value)
        print("Traceback:", exc_traceback)


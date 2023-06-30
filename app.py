from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension


"""
Step#1 
looking at app.py no flask code was given, we will insert our own. 
this is where your routing logic should go.
PAM: understood Will do!
"""

boggle_game = Boggle()

#flask requiered app name
app = Flask(__name__)

#flask debugtoolbar settings
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app) 



#GET
@app.route('/') #decorator expecting a function
def homepage(): #the function that will be executed when decorator is flagged
    """Show homepage"""


    # Keep a count of how many times page is visited
    session['count'] = session.get('count', 0) + 1
    # if its the users first time give them a thanks 
    if session['count'] == 1:
        flash('Hi Im Phedias, I hope you enjoy this game. Thanks for taking a look.')

    return render_template("home.html")

@app.route('/start-game')
def start_game():
    """ initialize game board for this session and redirect user to generated board page"""
    
    board = boggle_game.make_board()

    session['board'] = board

    return redirect('/game-board')

@app.route('/game-board')
def show_board():
    """Show the user the boggle board"""
    board = session.get('board')

    return render_template("board.html", board=board)
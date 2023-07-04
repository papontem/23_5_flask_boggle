from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import json, sys, traceback

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
    """
    Flasks Tests for our app.py where we'll test each routes logic.
    """
    # @classmethod
    # def setUpClass(cls):
    #     print("INSIDE SET UP CLASS")

    # @classmethod
    # def tearDownClass(cls):
    #     print("INSIDE TEAR DOWN CLASS")

    # def setUp(self):
    #     print("INSIDE SET UP")

    # def tearDown(self):
    #     print("INSIDE TEAR DOWN")


    def test_home(self):
        """ test user is being served the home template"""
        with app.test_client() as client:
            try:
                # Pythons Native Debugger here to help ^_^ !! 
                # import pdb
                # pdb.set_trace()

                res = client.get('/')
                html = res.get_data(as_text=True)

            except:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing of route to the homepage '/' ")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(res.status_code, 200)
                self.assertIn('<h2>Home</h2>', html)


    def test_start_game_redirection(self):
        """ test if user is corectly being redirected to the route /game-board"""
        with app.test_client() as client:
            try:
                resp = client.get("/start-game")
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing of redirection for route /start-game")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 302)
                self.assertEqual(resp.location, "http://localhost/game-board")

    def test_start_game_redirection_followed(self):
        """ test if user is corectly folowing the redirect from /start-game to /game-board """
        with app.test_client() as client:
            try:
            
            # # Any changes to session should go in here:
            # with client.session_transaction() as change_session:
            #     change_session['board'] = [
            #         ['A', 'B', 'C', 'D','E'],
            #         ['A', 'B', 'C', 'D','E'],
            #         ['A', 'B', 'C', 'D','E'],
            #         ['A', 'B', 'C', 'D','E'],
            #         ['A', 'B', 'C', 'D','E'],
            #     ]
                resp = client.get("/start-game", follow_redirects=True)
                html = resp.get_data(as_text=True)
            
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing of redirection being followed after route /start-game to route /game-board")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h2>Boggle Game Board</h2>', html)

    def test_game_board(self):
        """test whether route/game-board is responding with board template"""
        with app.test_client() as client:
            try:
                res = client.get('/game-board')
                html = res.get_data(as_text=True)
            
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing of game board route")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(res.status_code, 200)
                self.assertIn('<h2>Boggle Game Board</h2>', html)

    
    def test_guess_axios_request(self):
        """ 
        test what happens when we make request through route /guess using axios
        """
        with app.test_client() as client:
            res = client.get('/guess')

            try:
                res_data_json_str = res.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing of axios guess request, trying to get response data")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                # print("#########################")
                # print("Response =", res)
                # print("Response data JSON string = \n", res_data_json_str)
                # print("#########################")

                self.assertEqual(res.status_code, 200)
                self.assertIsInstance(res_data_json_str, str)


    
    def test_update_tracked_user_score(self):
        """ Test that user can record their highscores with the axios /score_update route"""
        with app.test_client() as client:
            with client.session_transaction() as session:
                session.clear()

            try:
                # create the payload
                payload = {"score": 100}

                # send POST request to the route
                res = client.post('/score_update', json=payload)
                # get the json string
                res_data_json_str = res.get_data(as_text=True)

                # verify the session by getting the highscore currently saved
                with client.session_transaction() as session:
                    highscore = session.get('highscore')

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing of axios highscore update request")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                # print("#########################")
                # print("response=",res)
                # print("response data json string = \n", res_data_json_str)
                # print("#########################")

                # verify the response
                self.assertEqual(res.status_code, 200)
                self.assertEqual(res.content_type, 'application/json')
                self.assertIsInstance(res_data_json_str, str)

                # verify the response JSON
                res_json = res.get_json()
                self.assertEqual(res_json, {"highscore": 100})
                
                # verify highscore
                self.assertEqual(highscore, 100)

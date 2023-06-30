from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    # PAM: understood! will do

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
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>Home</h2>', html)

    def test_start_game_redirection(self):
        with app.test_client() as client:
            resp = client.get("/start-game")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/game-board")

    def test_game_board(self):
        """test wether server is showing board"""
        with app.test_client() as client:
            res = client.get('/game-board')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>Boggle Game Board</h2>', html)



import unittest
from flask import json
from flask.json import jsonify
import flask_testing
from flask_sqlalchemy import SQLAlchemy
from app import *
from app import app,db

# Chu Wei Quan
class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    db.init_app(app)

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class test_final_quiz(unittest.TestCase):
    def test_get_quiz_id(self):
        fquiz = FinalQuiz(quiz_id = "1", passing_score = "85")
        self.assertEqual(fquiz.get_quiz_id(), "1")

    def test_get_passing_score(self):
        fquiz = FinalQuiz(quiz_id = "1", passing_score = "85")
        self.assertEqual(fquiz.get_passing_score(), "85")

class test_create_final_quiz(TestApp):  
    def test_create_final_quiz(self):
        quiz_id = "864"
        fquiz = FinalQuiz()
        status = fquiz.create_final_quiz(quiz_id)

        self.assertEqual(status[1], 200)

    def test_is_graded(self):
        fquiz = FinalQuiz(quiz_id = "678", passing_score = "85")
        db.session.add(fquiz)
        db.session.commit()

        quiz_id = fquiz.get_quiz_id()
        self.assertEqual(fquiz.is_graded(quiz_id)[0], 85)

        

if __name__ == '__main__':
    unittest.main()
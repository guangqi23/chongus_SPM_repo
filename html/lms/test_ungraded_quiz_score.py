import unittest
from flask import json
from flask.json import jsonify
import flask_testing
from flask_sqlalchemy import SQLAlchemy
from app import *
from app import app,db


#Coded by: Wang Xing Jie

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

class test_quiz_score(TestApp):
    def test_insert(self):

        inputObj = {'user_id': 4, 'quiz_id': 150, 'quiz_score': 100,  'time_inserted': datetime.now()}
        uqs = Ungraded_quiz_score()
        result = uqs.insert_score(inputObj)
        self.assertEqual(result, "Success")

    def test_check_attempt(self):
        gq = Ungraded_quiz_score(
            userid = 4,
            quiz_id = 150,
            quiz_score = 100,
            time_inserted = datetime.now() 
        )

        db.session.add(gq)
        db.session.commit()

        gqs = Ungraded_quiz_score()
        inputObj = {'user_id': 4, 'quiz_id': 150}
        result = gqs.checkAttempt(inputObj)
        self.assertEqual(result, "Yes")


if __name__ == '__main__':
    unittest.main()
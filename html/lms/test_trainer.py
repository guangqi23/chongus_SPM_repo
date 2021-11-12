import unittest
from flask import json
from flask.json import jsonify
import flask_testing
from flask_sqlalchemy import SQLAlchemy
from app import *
from app import app,db

#Ong Guang Qi
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


class test_Trainer_Assignment(unittest.TestCase):
    def test_get_course_id(self):
        ta1 = Trainer_Assignment(course_id = '1',
                                class_id = '1',
                                userid= '6')

        self.assertEqual(ta1.get_course_id(),'1')
    
    def test_get_class_id(self):
        ta1 = Trainer_Assignment(course_id = '1',
                                class_id = '1',
                                userid= '6')

        self.assertEqual(ta1.get_class_id(),'1')

    def test_get_user_id(self):
        ta1 = Trainer_Assignment(course_id = '1',
                                class_id = '1',
                                userid= '6')

        self.assertEqual(ta1.get_user_id(),'6')

class test_Assign_Controller(TestApp):
    def test_assign_course_trainer(self):
        trnr = Trainer(name = "Paul",
                        email = 'paultest@gmail.com',
                        department = 'SCIS',
                        designation = "Senior Engineer")
        db.session.add(trnr)
        db.session.commit()
        print(trnr)

        request_body = {
            'course_id' : 3,
            'class_id' : 2,
            'hr_id' : 1,
            'trainer_id' : trnr.userid
        }

        response = self.client.post("/assign_course_trainer",
                            data=json.dumps(request_body),
                            content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 200)

        

if __name__ == '__main__':
    unittest.main()





    


import unittest
from flask import json
from flask.json import jsonify
from flask import Flask, request, jsonify
import flask_testing
from flask_sqlalchemy import SQLAlchemy
from learner_assignment import Learner_Assignment
from learner import Learner
from trainer import Trainer
from trainer_assignment import Trainer_Assignment
from app import app, db


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

class test_Assign_Controller(TestApp):
    def test_assign_course_trainer(self):
        trnr = Trainer(name = "Paul",
                        email = 'paultest@gmail.com',
                        department = 'SCIS',
                        designation = "Senior Engineer")
        db.session.add(trnr)
        db.session.commit()

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


    def test_assign_course_learner(self):
        lrnr = Learner(name = "Jenny",
                        email = 'jennytest@gmail.com',
                        department = 'SCIS',
                        designation = "Junior Engineer")
        db.session.add(lrnr)
        db.session.commit()

        request_body = {
            'course_id' : 3,
            'class_id' : 2,
            'hr_id' : 1,
            'learner_id' : lrnr.userid
        }

        response = self.client.post("/assign_course_learner",
                            data=json.dumps(request_body),
                            content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_assigned_classes_trainer(self):
        trnr = Trainer(name = "Paul",
                        email = 'paultest@gmail.com',
                        department = 'SCIS',
                        designation = "Senior Engineer")
        db.session.add(trnr)
        db.session.commit()
        trnr_as = Trainer_Assignment(course_id = 3, class_id = 2, userid = trnr.userid)
        db.session.add(trnr_as)
        db.session.commit()

        request_body = {
            'userid' : trnr.userid
        }

        verifying_data = {"class 1":{"class_id":2,"course_id":3,"userid":trnr.userid}}

        response = self.client.post("/get_assigned_courses",
                            data=json.dumps(request_body),
                            content_type='application/json')

        responseData = json.loads(response.data.decode('utf-8'))
  
        self.assertEqual(responseData, verifying_data)


    def test_delete_assigned_classes(self):
        lrnr = Learner(name = "Jenny",
                        email = 'jennytest@gmail.com',
                        department = 'SCIS',
                        designation = "Junior Engineer")
        db.session.add(lrnr)
        db.session.commit()
        lrnr_as = Learner_Assignment(course_id = 3, class_id =2 , userid = lrnr.userid)
        db.session.add(lrnr_as)
        db.session.commit()

        request_body = {
            'course_id' : 3,
            'class_id' : 2,
            'userid' : lrnr.userid
        }

        response = self.client.post("/get_assigned_courses",
                            data=json.dumps(request_body),
                            content_type='application/json')

        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

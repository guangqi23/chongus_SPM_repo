import unittest
from flask import json
from flask.json import jsonify
from flask import Flask, request, jsonify
import flask_testing
from flask_sqlalchemy import SQLAlchemy
from app import *
from app import app,db
from json import JSONEncoder
from datetime import datetime, date

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

class test_app(TestApp):
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
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        db.session.close()


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
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        db.session.close()

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
        db.session.close()

    def test_get_all_classes(self):
        crse = Course(course_id = 5, 
                    course_name = 'testCourse',
                    course_description = 'testing our function',
                    startenrollmentdate = datetime(2021,10,6,0,0,0),
                    endenrollmentdate = datetime(2021,10,9,0,0,0))
        db.session.add(crse)
        db.session.commit()
        crse_class = Classes(class_id = 1 , course_id = crse.course_id, slots = 40 , startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,9,0,0,0), trainer_name = '')
        db.session.add(crse_class)
        db.session.commit()

        request_body = {
            'course_id' : crse.course_id
        }

        response = self.client.post("/get_classes/" + str(crse.course_id),
                        data=json.dumps(request_body),
                        content_type='application/json')


        self.assertEqual(response.status_code, 200)
        db.session.close()

    def test_delete_course(self):

        crse = Course(course_id = 919, 
                    course_name = 'testCourse',
                    course_description = 'testing our function',
                    startenrollmentdate = datetime(2021,10,8,0,0,0),
                    endenrollmentdate = datetime(2021,10,9,0,0,0))
        db.session.add(crse)
        db.session.commit()

        request_body = {
            'course_id' : crse.course_id
        }
        response = self.client.post("/delete_course",
                        data=json.dumps(request_body),
                        content_type='application/json')
        # print(response.data)
        # print("hello")
        self.assertEqual(response.status_code,200)
        db.session.close()

    #need test again
    def test_change_enrollment_status(self):
        crse_erlmt = Course_Enrollment(enrollment_id = 999,
                                         course_id = 999 ,
                                         userid = 999,
                                         class_id = 999 ,
                                         is_enrolled = 0) 
        
        db.session.add(crse_erlmt)
        db.session.commit()
        

        request_body = {
            'enrollment_id' : crse_erlmt.enrollment_id
        }

        response = self.client.post("/changeEnrollmentStatus",
                        data=json.dumps(request_body),
                        content_type='application/json')
                        
        
        self.assertEqual(crse_erlmt.is_enrolled,1)
        db.session.close()
  

    def test_reject_enrollment(self):
        crse_erlmt = Course_Enrollment(enrollment_id = 999,
                                         course_id = 999 ,
                                         userid = 999,
                                         class_id = 999 ,
                                         is_enrolled = 0) 

        db.session.add(crse_erlmt)
        db.session.commit()

        request_body = {
            'enrollment_id' : 999
        }

        response = self.client.post("/rejectEnrollment",
                        data=json.dumps(request_body),
                        content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        db.session.close()

    def test_enroll(self):

        crse = Course(course_id = 919, 
                    course_name = 'testCourse',
                    course_description = 'testing our function',
                    startenrollmentdate = datetime(2021,10,8,0,0,0),
                    endenrollmentdate = datetime(2021,10,9,0,0,0))

        cls = Classes(class_id = 999,
                    course_id = crse.course_id,
                    slots = 99,
                    startdate = datetime(2021,10,8,0,0,0),
                    enddate = datetime(2021,10,9,0,0,0),
                    trainer_name = 'Alex')

        db.session.add(crse)
        db.session.add(cls)
        db.session.commit()


        request_body = {
            'user_id' : 99,
            'class_id' : cls.class_id,
            'course_id' : crse.course_id
        } 

        response = self.client.post("/enroll",
                data=json.dumps(request_body),
                content_type='application/json')

        self.assertEqual(response.status_code, 200)
        db.session.close()

    def test_drop_class(self):
        crse_erlmt = Course_Enrollment(enrollment_id = 999,
                                         course_id = 999 ,
                                         userid = 999,
                                         class_id = 999 ,
                                         is_enrolled = 0) 
        db.session.add(crse_erlmt)
        db.session.commit()

        request_body = {
            'user_id' : crse_erlmt.userid,
            'class_id' : crse_erlmt.class_id,
            'course_id' : crse_erlmt.course_id
        }

        response = self.client.post("/drop_class",
                        data=json.dumps(request_body),
                        content_type='application/json')

        self.assertEqual(response.status_code,200)
        db.session.close()

    def test_create_quiz(self):
        
        with app.test_client() as c:
            r = c.get('/create_quiz', query_string={'section_id': '1', 'time_limit': "60"})

        self.assertEqual(r.status_code,200)


    def test_create_section_materials(self):

        with app.test_client() as c:
            r = c.get('/create_section_materials', query_string={'section_id': '1',
             'material_title': "test_material_title",
             "material_content": "test_material_content",
             "material_type": "test_material_type"})
        print(r.data)
        self.assertEqual(r.status_code,200)


    def test_create_TrueFalse(self):

        with app.test_client() as c:
            r = c.get('/create_TrueFalse', query_string={'answer': '1',
             'quiz_id': "2",
             "qorder": "1",
             "question_type": "test_question_type",
             'question' : "test_question"})
        print(r.data)
        self.assertEqual(r.status_code,200)

    def test_create_MCQ_Question(self):

        with app.test_client() as c:
            r = c.get('/create_MCQ_Question', query_string={
             'quiz_id': "2",
             "qorder": "1",
             "question_type": "test_question_type",
             'question' : "test_question"})
        print(r.data)
        self.assertEqual(r.status_code,200)

    def test_add_MCQ_option(self):
        with app.test_client() as c:
            r = c.get('/add_MCQ_Options', query_string={
             'question_id': "99",
             "option_order": "4",
             "option_content": "test_option_content",
             'correct_option' : "1"})
        
        print(r.data)
        self.assertEqual(r.status_code,200)

    def test_submitScore(self):
        with app.test_client() as c:
            r = c.post('/submitScore', query_string={
             'quiz_id': "99",
             "user_id": "4",
             "score": "4.0"})
        print(r)
        self.assertEqual(r.status_code,200)

if __name__ == '__main__':
    unittest.main()

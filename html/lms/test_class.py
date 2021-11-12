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

#Tok Tze Kiat
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
        

class test_Class(TestApp):
    def test_get_course_id(self):
        crse = Course(course_id = 8, 
                    course_name = 'test class course',
                    course_description = 'testing course',
                    startenrollmentdate = datetime(2021,10,6,0,0,0),
                    endenrollmentdate = datetime(2021,10,9,0,0,0))
        crse_class = Classes(class_id = 1,
                        course_id = crse.course_id,
                        slots = 40,
                        startdate = datetime(2021,10,6,0,0,0),
                        enddate = datetime(2021,10,9,0,0,0),
                        trainer_name = '')
        self.assertEqual(crse_class.course_id,8)
        
        
        def test_get_course_id(self):
            crse = Course(course_id = 8, 
                        course_name = 'test class course',
                        course_description = 'testing course',
                        startenrollmentdate = datetime(2021,10,6,0,0,0),
                        endenrollmentdate = datetime(2021,10,9,0,0,0))
            crse_class = Classes(class_id = 1,
                            course_id = crse.course_id,
                            slots = 40,
                            startdate = datetime(2021,10,6,0,0,0),
                            enddate = datetime(2021,10,9,0,0,0),
                            trainer_name = '')
            self.assertEqual(crse_class.course_id,8)
        
    def test_get_class_id(self):
        crse = Course(course_id = 8, 
                    course_name = 'test class course',
                    course_description = 'testing course',
                    startenrollmentdate = datetime(2021,10,6,0,0,0),
                    endenrollmentdate = datetime(2021,10,9,0,0,0))
        crse_class = Classes(class_id = 1,
                        course_id = crse.course_id,
                        slots = 40,
                        startdate = datetime(2021,10,6,0,0,0),
                        enddate = datetime(2021,10,9,0,0,0),
                        trainer_name = '')
        self.assertEqual(crse_class.class_id,1)
        
    def test_get_slot(self):
        crse = Course(course_id = 8, 
                    course_name = 'test class course',
                    course_description = 'testing course',
                    startenrollmentdate = datetime(2021,10,6,0,0,0),
                    endenrollmentdate = datetime(2021,10,9,0,0,0))
        crse_class = Classes(class_id = 1,
                        course_id = crse.course_id,
                        slots = 40,
                        startdate = datetime(2021,10,6,0,0,0),
                        enddate = datetime(2021,10,9,0,0,0),
                        trainer_name = '')
        self.assertEqual(crse_class.slots,40)
        
    def test_get_course_id(self):
        crse = Course(course_id = 8, 
                    course_name = 'test class course',
                    course_description = 'testing course',
                    startenrollmentdate = datetime(2021,10,6,0,0,0),
                    endenrollmentdate = datetime(2021,10,9,0,0,0))
        crse_class = Classes(class_id = 1,
                        course_id = crse.course_id,
                        slots = 40,
                        startdate = datetime(2021,10,6,0,0,0),
                        enddate = datetime(2021,10,9,0,0,0),
                        trainer_name = 'John Xina')
        self.assertEqual(crse_class.trainer_name,'John Xina')
        
    def test_get_course_id(self):
            crse = Course(course_id = 8, 
                        course_name = 'test class course',
                        course_description = 'testing course',
                        startenrollmentdate = datetime(2021,10,6,0,0,0),
                        endenrollmentdate = datetime(2021,10,9,0,0,0))
            crse_class = Classes(class_id = 1,
                            course_id = crse.course_id,
                            slots = 40,
                            startdate = datetime(2021,10,6,0,0,0),
                            enddate = datetime(2021,10,9,0,0,0),
                            trainer_name = '')
            self.assertEqual(crse_class.course_id,8)
        
    def test_class_slots(self):
        crse = Course(course_id = 8, 
                    course_name = 'test class course',
                    course_description = 'testing course',
                    startenrollmentdate = datetime(2021,10,6,0,0,0),
                    endenrollmentdate = datetime(2021,10,9,0,0,0))
        db.session.add(crse)
        db.session.commit()
        crse_class = Classes(class_id = 1, course_id = crse.course_id, slots = 40 , startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,9,0,0,0), trainer_name = '')
        db.session.add(crse_class)
        db.session.commit()
        class_info = crse_class.get_classes_by_cid(1,8)
        values = json.loads(class_info.data)
        self.assertEqual(values['data']['slots'],40)
        
    def test_class_by_class_id(self):
        crse = Course(course_id = 8, 
                    course_name = 'test class course',
                    course_description = 'testing course',
                    startenrollmentdate = datetime(2021,10,6,0,0,0),
                    endenrollmentdate = datetime(2021,10,9,0,0,0))
        db.session.add(crse)
        db.session.commit()
        crse_class = Classes(class_id = 1 , course_id = crse.course_id, slots = 40 , startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,9,0,0,0), trainer_name = '')
        db.session.add(crse_class)
        db.session.commit()
        cid = crse_class.get_classes_by_class_id(crse_class.course_id,crse_class.class_id)
        self.assertEqual(cid,crse_class)
        
    def test_class_by_class_id(self):
        crse = Course(course_id = 8, 
                    course_name = 'test class course',
                    course_description = 'testing course',
                    startenrollmentdate = datetime(2021,10,6,0,0,0),
                    endenrollmentdate = datetime(2021,10,9,0,0,0))
        db.session.add(crse)
        db.session.commit()
        crse_class = Classes(class_id = 1 , course_id = crse.course_id, slots = 40 , startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,9,0,0,0), trainer_name = '')
        db.session.add(crse_class)
        db.session.commit()
        startdate = crse_class.get_class_startdate(crse_class.class_id)
        startdate_dt =  datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
        self.assertEqual(startdate_dt,crse_class.startdate)

    def test_class_by_class_id(self):
        crse = Course(course_id = 8, 
                    course_name = 'test class course',
                    course_description = 'testing course',
                    startenrollmentdate = datetime(2021,10,6,0,0,0),
                    endenrollmentdate = datetime(2021,10,9,0,0,0))
        db.session.add(crse)
        db.session.commit()
        crse_class = Classes(class_id = 1 , course_id = crse.course_id, slots = 40 , startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,9,0,0,0), trainer_name = '')
        db.session.add(crse_class)
        db.session.commit()
        cid = crse_class.get_classes_by_course(crse.course_id)
        c_list =[]
        c_list.append(crse_class)
        self.assertEqual(cid,c_list)
        
if __name__ == '__main__':
    unittest.main()
        
    

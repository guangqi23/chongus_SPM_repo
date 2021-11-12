import unittest
from flask import json
from flask.json import jsonify
import flask_testing
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import *
from app import app, db

#Done by Wu Jiafang
class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    db.init_app(app)

    def setUp(self):
        # self.learner1 = Learner(name = "Paul", email = 'paultest@gmail.com', department = 'SCIS', designation = "Junior Engineer")
        # self.course1 = Course(course_id = 21, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10900', 
        # startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        # self.class1 = Classes(class_id = 1, course_id = 21, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')
        # self.assigned_course1 = Learner_Assignment(course_id = 21, class_id = 1, userid = self.learner1.userid)
        db.session.commit()
        db.create_all()

    def create_app(self):
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class test_Learner_info(TestApp):
    def test_get_all_learners(self):
        learner1 = Learner(name = "Paul", email = 'paultest@gmail.com', department = 'SCIS', designation = "Junior Engineer")
        learner2 = Learner(name = "Mary", email = 'marytest@gmail.com', department = 'SOB', designation = "Senior Engineer")
        db.session.add(learner1)
        db.session.add(learner2)
        db.session.commit()
        self.assertEqual(learner1.get_all_learners(), [learner1, learner2])
    
    def test_get_all_learners_ids(self):
        learner3 = Learner(name = "Bob", email = 'bobtest@gmail.com', department = 'SCIS', designation = "Junior Engineer")
        learner4 = Learner(name = "Jane", email = 'janetest@gmail.com', department = 'SOB', designation = "Senior Engineer")
        db.session.add(learner3)
        db.session.add(learner4)
        db.session.commit()
        self.assertEqual(learner3.get_all_learners_id(), [(1,), (2,)])

class test_Learner_Courses(TestApp):

    def test_get_assigned_courses(self):
        learner1 = Learner(name = "Paul", email = 'paultest@gmail.com', department = 'SCIS', designation = "Junior Engineer")
        db.session.add(learner1)
        db.session.commit()

        course1 = Course(course_id = 1, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10900', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        db.session.add(course1)
        db.session.commit()

        class1 = Classes(class_id = 1, course_id = 1, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')
        
        db.session.add(class1)
        db.session.commit()

        assigned_course1 = Learner_Assignment(course_id = 21, class_id = 21, userid = learner1.userid)

        db.session.add(assigned_course1)

        db.session.commit()
        self.assertEqual(learner1.get_assigned_courses(learner1.userid), [assigned_course1])

    def test_get_assigned_course_class(self):
        learner1 = Learner(name = "Paul", email = 'paultest@gmail.com', department = 'SCIS', designation = "Junior Engineer")
        db.session.add(learner1)
        db.session.commit()
        course1 = Course(course_id = 1, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10900', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        db.session.add(course1)
        db.session.commit()
        class1 = Classes(class_id = 1, course_id = 1, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')
        db.session.add(class1)
        db.session.commit()
        assigned_course1 = Learner_Assignment(course_id = 1, class_id = 1, userid = learner1.userid)
        db.session.add(assigned_course1)
        db.session.commit()
        
        self.assertEqual(learner1.get_assigned_course_class(learner1.userid), [[course1],[class1]])
    
    def test_get_enrolled_courses(self):
        learner2 = Learner(name = "Mary", email = 'marytest@gmail.com', department = 'SOB', designation = "Senior Engineer")
        db.session.add(learner2)
        db.session.commit()
        course1 = Course(course_id = 2, course_name = 'M102', course_description = 'Fundamentals of printing lessons for Printer Model MN10910', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        db.session.add(course1)
        db.session.commit()
        enrolled_course1 = Course_Enrollment(enrollment_id = 1, course_id = 2, userid = learner2.userid, class_id = 2, is_enrolled = True)
        db.session.add(enrolled_course1)
        db.session.commit()

        self.assertEqual(learner2.get_enrolled_courses(learner2.userid), [enrolled_course1])
    
    def test_get_enrolled_course_class(self):
        learner2 = Learner(name = "Megan", email = 'megantest@gmail.com', department = 'SOB', designation = "Junior Engineer")
        db.session.add(learner2)
        db.session.commit()
        course1 = Course(course_id = 21, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10900', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        db.session.add(course1)
        db.session.commit()
        class1 = Classes(class_id = 22, course_id = 21, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Benjamin Tan')
        db.session.add(class1)
        db.session.commit()
        enrolled_course1 = Course_Enrollment(enrollment_id = 1, course_id = 21, userid = learner2.userid, class_id = 22, is_enrolled = True)

        db.session.add(enrolled_course1)
        db.session.commit()

        self.assertEqual(learner2.get_enrolled_course_class(learner2.userid), [[course1],[class1]])
    
    def test_get_completed_courses(self):
        learner1 = Learner(name = "Paul", email = 'paultest@gmail.com', department = 'SCIS', designation = "Junior Engineer")
        db.session.add(learner1)
        db.session.commit()

        course1 = Course(course_id = 21, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10900', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        db.session.add(course1)
        db.session.commit()

        completed_course1 = Learner_Badges(userid = learner1.userid, course_id = 21)
        db.session.add(completed_course1)

        db.session.commit()
        self.assertEqual(learner1.get_completed_courses(learner1.userid), [course1])
    
    def test_get_remaining_courses(self):
        learner1 = Learner(name = "Paul", email = 'paultest@gmail.com', department = 'SCIS', designation = "Junior Engineer")
        db.session.add(learner1)
        db.session.commit()

        course1 = Course(course_id = 21, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10901', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course2 = Course(course_id = 22, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10902', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course3 = Course(course_id = 23, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10903', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course4 = Course(course_id = 24, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10904', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))

        class1 = Classes(class_id = 1, course_id = 21, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')
        class2 = Classes(class_id = 2, course_id = 22, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Chou')
        class3 = Classes(class_id = 3, course_id = 23, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Ben Nam')
        class4 = Classes(class_id = 4, course_id = 24, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Nick Nam')

        db.session.add(course1)
        db.session.add(course2)
        db.session.add(course3)
        db.session.add(course4)
        db.session.add(class1)
        db.session.add(class2)
        db.session.add(class3)
        db.session.add(class4)
        db.session.commit()

        completed_course1 = Learner_Badges(userid = learner1.userid, course_id = 21)
        db.session.add(completed_course1)
        assigned_course1 = Learner_Assignment(course_id = 22, class_id = 21, userid = learner1.userid)
        db.session.add(assigned_course1)
        enrolled_course1 = Course_Enrollment(enrollment_id = 1, course_id = 23, userid = learner1.userid, class_id = 21, is_enrolled = True)
        db.session.add(enrolled_course1)
    
        db.session.commit()
        self.assertEqual(learner1.get_remaining_courses(learner1.userid), [course4])
    
    def test_get_eligible_courses(self):
        learner1 = Learner(name = "Paul", email = 'paultest@gmail.com', department = 'SCIS', designation = "Junior Engineer")
        db.session.add(learner1)
        db.session.commit()

        course1 = Course(course_id = 21, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10901', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course2 = Course(course_id = 22, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10902', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course3 = Course(course_id = 23, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10903', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course4 = Course(course_id = 24, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10904', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))

        class1 = Classes(class_id = 1, course_id = 21, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')
        class2 = Classes(class_id = 2, course_id = 22, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Chou')
        class3 = Classes(class_id = 3, course_id = 23, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Tb')
        class4 = Classes(class_id = 4, course_id = 24, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')

        db.session.add(course1)
        db.session.add(course2)
        db.session.add(course3)
        db.session.add(course4)
        db.session.add(class1)
        db.session.add(class2)
        db.session.add(class3)
        db.session.add(class4)
        db.session.commit()

        completed_course1 = Learner_Badges(userid = learner1.userid, course_id = 21)
        db.session.add(completed_course1)
        assigned_course1 = Learner_Assignment(course_id = 22, class_id = 21, userid = learner1.userid)
        db.session.add(assigned_course1)
        enrolled_course1 = Course_Enrollment(enrollment_id = 1, course_id = 23, userid = learner1.userid, class_id = 21, is_enrolled = True)
        db.session.add(enrolled_course1)
    
        db.session.commit()
        self.assertEqual(learner1.get_eligible_courses(learner1.userid), [course4])

    def test_get_eligible_classes(self):
        learner1 = Learner(name = "Paul", email = 'paultest@gmail.com', department = 'SCIS', designation = "Junior Engineer")
        db.session.add(learner1)
        db.session.commit()

        course1 = Course(course_id = 21, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10901', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course2 = Course(course_id = 22, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10902', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course3 = Course(course_id = 23, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10903', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course4 = Course(course_id = 24, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10904', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))

        class1 = Classes(class_id = 1, course_id = 21, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')
        class2 = Classes(class_id = 2, course_id = 22, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')
        class3 = Classes(class_id = 3, course_id = 23, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')
        class4 = Classes(class_id = 4, course_id = 24, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')

        db.session.add(course1)
        db.session.add(course2)
        db.session.add(course3)
        db.session.add(course4)
        db.session.add(class1)
        db.session.add(class2)
        db.session.add(class3)
        db.session.add(class4)
        db.session.commit()

        completed_course1 = Learner_Badges(userid = learner1.userid, course_id = 21)
        db.session.add(completed_course1)
        assigned_course1 = Learner_Assignment(course_id = 22, class_id = 21, userid = learner1.userid)
        db.session.add(assigned_course1)
        enrolled_course1 = Course_Enrollment(enrollment_id = 1, course_id = 23, userid = learner1.userid, class_id = 21, is_enrolled = True)
        db.session.add(enrolled_course1)
    
        db.session.commit()
        self.assertEqual(learner1.get_eligible_classes(learner1.userid), [[course4],[class4]])

    def test_get_uneligible_course_class(self):
        learner1 = Learner(name = "Paul", email = 'paultest@gmail.com', department = 'SCIS', designation = "Junior Engineer")
        db.session.add(learner1)
        db.session.commit()

        course1 = Course(course_id = 21, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10900', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course2 = Course(course_id = 22, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10900', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course3 = Course(course_id = 23, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10900', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course4 = Course(course_id = 24, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10900', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))
        course5 = Course(course_id = 25, course_name = 'M101', course_description = 'Fundamentals of printing lessons for Printer Model MN10900', 
        startenrollmentdate = datetime(2021,10,6,0,0,0), endenrollmentdate = datetime(2021,11,6,0,0,0))

        class1 = Classes(class_id = 1, course_id = 21, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')
        class2 = Classes(class_id = 2, course_id = 22, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')
        class3 = Classes(class_id = 3, course_id = 23, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')
        class4 = Classes(class_id = 4, course_id = 24, slots = 2, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')
        class5 = Classes(class_id = 5, course_id = 25, slots = 0, startdate = datetime(2021,10,6,0,0,0), enddate = datetime(2021,10,30,0,0,0), trainer_name = 'Eric Nam')

        course_prequisite1 = Course_Prerequisites(course_id = 25, prereq_course_id = 24) 

        db.session.add(course1)
        db.session.add(course2)
        db.session.add(course3)
        db.session.add(course4)
        db.session.add(course5)
        db.session.add(class1)
        db.session.add(class2)
        db.session.add(class3)
        db.session.add(class4)
        db.session.add(class5)
        db.session.add(course_prequisite1)
        db.session.commit()

        completed_course1 = Learner_Badges(userid = learner1.userid, course_id = 21)
        db.session.add(completed_course1)
        assigned_course1 = Learner_Assignment(course_id = 22, class_id = 2, userid = learner1.userid)
        db.session.add(assigned_course1)
        enrolled_course1 = Course_Enrollment(enrollment_id = 1, course_id = 23, userid = learner1.userid, class_id = 3, is_enrolled = True)
        db.session.add(enrolled_course1)
    
        db.session.commit()
        self.assertEqual(learner1.get_uneligible_course_class(learner1.userid), [[course5],[class5]])

if __name__ == '__main__':
    unittest.main()
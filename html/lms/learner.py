from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import false, true
from user import User
from course import Course
from course_enrollment import Course_Enrollment
from course_prerequisites import Course_Prerequisites
from learner_assignment import Learner_Assignment
from learner_badges import Learner_Badges

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class Learner(User):
    __tablename__ = 'learners'

    __mapper_args__ = {'polymorphic_identity': 'learner'}

    def get_all_learners(self):
        lrnr = Learner()
        return lrnr.query.filter_by(designation='Learner').all()

    def get_all_learners_id(self):
        lrnr = Learner()
        records = Learner.query.with_entities(Learner.userid).all()
        print(records)
        return records

    def get_remaining_courses(self, userid):
        learner_badges = Learner_Badges()
        course_class = Course()

        course_list = [course.course_id for course in course_class.get_all_courses()]
        completed_courses = [course.course_id for course in learner_badges.get_learner_badges(userid)]
        enrolled_courses = [course.course_id for course in self.get_enrolled_courses(userid)]
        assigned_courses = [course.course_id for course in self.get_assigned_courses(userid)]
        completed_enrolled_assigned_courses = completed_courses + enrolled_courses + assigned_courses
        remaining_course = [course for course in course_list if course not in completed_enrolled_assigned_courses]

        output = []

        for course_query in remaining_course: 
            vacancies = course_class.get_vacancies_by_courses(course_query)
            if vacancies > 0: 
                    courseinfo = course_class.get_course_by_id(course_query)
                    output.append(courseinfo)

        return output

    def get_eligible_courses(self, userid):
        course_class = Course()
        course_pre_req = Course_Prerequisites()
        learner_badges = Learner_Badges()
        completedcourses = learner_badges.get_learner_badges(userid)

        course_list = [course.course_id for course in self.get_remaining_courses(userid)]
        
        output = []

        for course_query in course_list: 
            prereqlist = course_pre_req.prereq_by_course(course_query)
            if len(prereqlist) == 0: 
                courseinfo = course_class.get_course_by_id(course_query)
                output.append(courseinfo)
            else: 
                for course in prereqlist: 
                    if course.prereq_course_id in completedcourses:
                        courseinfo = course_class.get_course_by_id(course_query)
                        output.append(courseinfo)
        
        return output

    def get_uneligible_courses(self, userid):
        course_class = Course()

        course_list = [course.course_id for course in self.get_remaining_courses(userid)]
        eligible_courses = [course.course_id for course in self.get_eligible_courses(userid)]
        other_courses = [course for course in course_list if course not in eligible_courses]

        output = []
      
        for course_query in other_courses: 
            courseinfo = course_class.get_course_by_id(course_query)
            output.append(courseinfo)

        return output
    
    def is_learner(self, user_id):
        lrnr = Learner.query.filter_by(userid=user_id).first()
        return lrnr
    
    def get_enrolled_courses(self, user_id): 
        enrolled_courses_list = self.get_enrolled_classes(user_id)
        course_class = Course()
        output = []

        for enrolled_course in enrolled_courses_list:
            courseinfo = course_class.get_course_by_id(enrolled_course.course_id)
            output.append(courseinfo)

        return output

    def get_enrolled_classes(self, user_id):
        enrolled_courses = Course_Enrollment()
        enrolled_courses_list = enrolled_courses.get_user_enrolled_courses(user_id)
        print(enrolled_courses_list)
        
        output = []
        for enrolled_course in enrolled_courses_list:
            if enrolled_course.is_enrolled == 1:
                output.append(enrolled_course)

        return output

    def get_assigned_courses(self, user_id): 
        assigned_courses = Learner_Assignment()
        course_class = Course()
        output = []
        assigned_courses_list = assigned_courses.get_user_assigned_courses(user_id)
        for assigned_course in assigned_courses_list:
            courseinfo = course_class.get_course_by_id(assigned_course.course_id)
            output.append(courseinfo)
        return output
    
    def get_completed_courses(self, user_id):
        completed_courses = Learner_Badges()
        course_class = Course()
        output = []
        completed_courses_list = completed_courses.get_learner_badges(user_id)
        for completed_course in completed_courses_list:
            courseinfo = course_class.get_course_by_id(completed_course.course_id)
            output.append(courseinfo)
        return output




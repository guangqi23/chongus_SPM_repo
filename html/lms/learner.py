from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import false, true
from classes import Classes
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
        records = Learner.query.filter_by(designation='Junior Engineer').all()
        records2 = Learner.query.filter_by(designation='Senior Engineer').all()
        records3 = records + records2
        return records3

    def get_all_learners_id(self):
        records = Learner.query.with_entities(Learner.userid).all()
        return records
    
    def is_learner(self, user_id):
        lrnr = Learner.query.filter_by(userid=user_id).first()
        return lrnr
    
    def get_course_class (self, course_list):
        course_class = Course()
        classes_class = Classes()
        courses = [course_class.get_course_by_id(a_course.course_id) for a_course in course_list]
        classes = []
        for a_course in course_list:
            classinfo = classes_class.get_classes_by_class_id(a_course.course_id, a_course.class_id)
            for a_class in classinfo:
                classes.append(a_class)
        return [courses, classes]
    
    def get_enrolled_courses(self, user_id):
        enrolled_courses = Course_Enrollment()
        enrolled_courses_list = enrolled_courses.get_user_enrolled_courses(user_id)        
        output = [enrolled_course for enrolled_course in enrolled_courses_list if enrolled_course.is_enrolled == 1]
        return output
    
    def get_enrolled_course_class(self, user_id): 
        enrolled_courses_list = self.get_enrolled_courses(user_id)  
        output = [enrolled_course for enrolled_course in enrolled_courses_list]
        return output

    def get_assigned_courses(self, user_id): 
        assigned_courses = Learner_Assignment()
        assigned_courses_list = assigned_courses.get_user_assigned_courses(user_id)
        output = [assigned_course for assigned_course in assigned_courses_list]
        return output
    
    def get_assigned_course_class(self, user_id): 
        assigned_courses = Learner_Assignment()
        assigned_courses_list = assigned_courses.get_user_assigned_courses(user_id)
        output = self.get_course_class(assigned_courses_list)
        return output

    def get_completed_courses(self, user_id):
        completed_courses = Learner_Badges()
        course_class = Course()
        completed_courses_list = completed_courses.get_learner_badges(user_id)
        output = [course_class.get_course_by_id(completed_course.course_id) for completed_course in completed_courses_list]
        return output

    def get_remaining_courses(self, user_id):
        learner_badges = Learner_Badges()
        course_class = Course()
        course_list = [course.course_id for course in course_class.get_all_courses()]
        completed_courses = [course.course_id for course in learner_badges.get_learner_badges(user_id)]
        enrolled_courses = [course for course in self.get_enrolled_courses(user_id)]
        assigned_courses = [course for course in self.get_assigned_courses(user_id)]
        completed_enrolled_assigned_courses = completed_courses + enrolled_courses + assigned_courses
        remaining_course = [course for course in course_list if course not in completed_enrolled_assigned_courses]
        output = [course_class.get_course_by_id(course_query) for course_query in remaining_course if course_class.get_vacancies_by_courses(course_query) > 0]
        return output

    def get_eligible_courses(self, user_id):
        course_pre_req = Course_Prerequisites()
        learner_badges = Learner_Badges()
        completed_courses = learner_badges.get_learner_badges(user_id)

        course_list = [course.course_id for course in self.get_remaining_courses(user_id)]
        course_query_list = []

        for course_query in course_list: 
            prereqlist = course_pre_req.prereq_by_course(course_query)
            if len(prereqlist) == 0: 
                course_query_list.append(course_query)
            else: 
                for course in prereqlist: 
                    if course.prereq_course_id in completed_courses:
                        course_query_list.append(course_query)
        
        return course_query_list

    def get_eligible_classes(self, user_id):
        course_class = Course()
        classes_class = Classes()
        course_query_list = self.get_eligible_courses(user_id)
        courses = []
        classes = []
        for course in course_query_list:
            course_classes = classes_class.get_classes_by_course(course)
            for a_class in course_classes:
                if a_class.slots > 0: 
                    course_info = course_class.get_course_by_id(course)
                    courses.append(course_info)
                    classes.append(a_class)
        
        return [courses, classes]

    def get_uneligible_courses(self, user_id):
        course_class = Course()
        course_list = [course.course_id for course in self.get_remaining_courses(user_id)]
        eligible_courses = [course for course in self.get_eligible_courses(user_id)]
        other_courses = [course for course in course_list if course not in eligible_courses]
        output = [course_class.get_course_by_id(course_query) for course_query in other_courses]
        return output

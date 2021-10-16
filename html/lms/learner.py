from flask import Flask, request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy.sql.expression import false, true
from learner_badges import learnerbadges
from user import User
from course import Course
from course_prerequisites import Course_Prerequisites
from sqlalchemy import Column, Integer
from course_enrollment import Course_Enrollment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class Learner_Assignment(db.Model):
    __tablename__ = 'LEARNERASSIGNMENT'

    course_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, primary_key=True, index=True)
    userid = db.Column(db.Integer, primary_key=True, index=True)

    def get_user_assigned_courses(self, userid): 
        record = Learner_Assignment.query.filter_by(userid=userid).all()
        return record
    
    def json(self):
        return {"course_id":self.course_id,"class_id":self.class_id, "userid":self.userid}

class Learner(User):
    __tablename__ = 'learners'

    __mapper_args__ = {'polymorphic_identity': 'learner'}


    def get_available_courses(self, userid):
        learner_badges = learnerbadges()
        prereq_class = Course_Prerequisites()
        course_class = Course()

        completedcourses = learner_badges.get_completed_courses(userid)
        all_courses = course_class.get_all_courses()
        
        course_list = []
        course_to_not_take = []

        for course in all_courses: 
            course_list.append(course.course_id)

        for course in completedcourses: 
            course_to_not_take.append(course.course_id)
        
        avail_course = [course for course in course_list if course not in course_to_not_take]

        output = []

        for course_query in avail_course: 
            prereqlist = prereq_class.prereq_by_course(course_query)
            vacancies = course_class.get_vacancies_by_courses(course_query)
            if vacancies > 0: 
                for course in prereqlist: 
                    if course.prereq_course_id not in completedcourses:
                        courseinfo = course_class.get_course_by_id(course_query)
                        output.append(courseinfo)

        return output
    
    def is_learner(self, user_id):
        lrnr = Learner.query.filter_by(userid=user_id).first()
        return lrnr
    
    def get_enrolled_courses(self, user_id): 
        enrolled_courses = Course_Enrollment()
        course_class = Course()
        output = []
        enrolled_courses_list = enrolled_courses.get_user_enrolled_courses(user_id)
        for enrolled_course in enrolled_courses_list:
            enrollment_status = enrolled_course.is_enrolled
            if enrollment_status:
                courseinfo = course_class.get_course_by_id(enrolled_course.course_id)
                output.append(courseinfo)
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

@app.route("/availcourses", methods=['POST'])
def get_available_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_available_courses(user_id)
    if len(record):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "record": [a_record.json() for a_record in record]
                    }
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "There are no available courses."
            }
        ), 404
    
@app.route("/enrolled_courses", methods=['POST'])
def get_enrolled_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_enrolled_courses(user_id)
    if len(record):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "record": [a_record.json() for a_record in record]
                    }
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "There are no enrolled courses."
            }
        ), 404

@app.route("/assigned_courses", methods=['POST'])
def get_assigned_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_assigned_courses(user_id)
    if len(record):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "record": [a_record.json() for a_record in record]
                    }
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "There are no assigned courses."
            }
        ), 404

if __name__ == '__main__':
    app.run(port=5002, debug=True)

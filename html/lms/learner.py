from flask import Flask, request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy.sql.expression import false, true
from learner_badges import learnerbadges
from user import User
from course import Course, Course_Prerequisites
from sqlalchemy import Column, Integer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class Learner(User):
    __tablename__ = 'learners'
    __mapper_args__ = {'polymorphic_identity': 'learner'}

    @declared_attr
    def user_id(cls):
        return User.__table__.c.get('user_id', Column(Integer))

    def get_available_courses(self, userid):
        learner_badges = learnerbadges()
        course_class = Course_Prerequisites()
        completedcourses = learner_badges.get_completed_courses(userid)
        all_courses = Course.get_all_courses()
        
        course_list = []
        course_to_not_take = []
        prereq = []

        print(all_courses)
        for course in all_courses: 
            course_list.append(course.course_id)

        for course in completedcourses: 
            course_to_not_take.append(course.course_id)
        
        avai_course = [course for course in course_list if course not in course_to_not_take]

        output = []

        for course_query in avai_course: 
            prereqlist = course_class.prereq_by_course(course_query)
            for course in prereqlist: 
                prereq.append(course.prereq_course_id)
                toadd = true
                for course in prereq:
                    if course not in completedcourses:
                        toadd= false 
                if toadd:
                    output.append(course_query)
                
        return output
    
    def is_learner(self, user_id):
        lrnr = Learner.query.filter_by(user_id=user_id).first()
        return lrnr

@app.route("/availcourses", methods=['POST'])
def get_available_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_available_courses(user_id)
    availcourses_json = json.dumps(record)
    if len(availcourses_json):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "avail_courses": availcourses_json
                    }
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "There are no avilable courses."
            }
        ), 404

if __name__ == '__main__':
    app.run(port=5002, debug=True)

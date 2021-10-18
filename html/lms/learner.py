from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import false, true
from learner_badges import learnerbadges
from user import User
from course import Course
from course_enrollment import Course_Enrollment
from course_prerequisites import Course_Prerequisites

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/lmsdb'
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

    def get_remaining_courses(self, userid):
        learner_badges = learnerbadges()
        course_class = Course()

        course_list = [course.course_id for course in course_class.get_all_courses()]
        completed_courses = [course.course_id for course in learner_badges.get_completed_courses(userid)]
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
        learner_badges = learnerbadges()
        completedcourses = learner_badges.get_completed_courses(userid)

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

@app.route("/eligible_courses", methods=['POST'])
def get_eligible_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_eligible_courses(user_id)
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
            "message": "There are no eligible courses."
            }
        ), 404

@app.route("/uneligible_courses", methods=['POST'])
def get_uneligible_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_uneligible_courses(user_id)
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
            "message": "There are no uneligible courses."
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

@app.route("/enrolled_classes", methods=["POST"])
def get_enrolled_classes():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_enrolled_classes(user_id)
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
            "message": "There are no enrolled classes."
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

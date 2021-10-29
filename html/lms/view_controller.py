from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.sql.expression import false, true
from flask_sqlalchemy import SQLAlchemy
from trainer import Trainer
from learner import Learner
from trainer_assignment import Trainer_Assignment
from learner_badges import learnerbadges
from course import Course
from classes import Classes
from learner_badges import Learner_Badges

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class ViewController():
    def get_courses_with_classes_without_trainer():
        trnr_as_class = Trainer_Assignment()
        course_class = Course()
        classes_class = Classes()

        course_list = [course.course_id for course in course_class.get_all_courses()]
        courses_with_trainers = [(course.course_id, course.class_id) for course in trnr_as_class.get_all_trainer_assignments()]

        crse_with_class_without_trainers = []
        output = []

        for crse in course_list:
            classesOfCrseList = [classes.class_id for classes in classes_class.get_classes_by_course(crse)] 
            
            for cl in classesOfCrseList:
                if (crse,cl) not in courses_with_trainers:
                    if(crse not in output):
                        crse_with_class_without_trainers.append(crse)
        
        for crse in crse_with_class_without_trainers:
            output.append(course_class.get_course_by_id(crse))

        print(output)
        
        return output

    def get_classes_of_a_course_without_trainer(course_id):
        trnr_as_class = Trainer_Assignment()
        course_class = Course()
        classes_class = Classes()

        courses_with_trainers = [(course.course_id, course.class_id) for course in trnr_as_class.get_all_trainer_assignments()]
        classesOfCrseList = [classes.class_id for classes in classes_class.get_classes_by_course(course_id)] 
        output = []
        classes_without_trainer = []
        for cl in classesOfCrseList:
                if (course_id,cl) not in courses_with_trainers:
                    if(cl not in output):
                        classes_without_trainer.append(cl)
                        
        print(classes_without_trainer)
        for cl in classes_without_trainer:
            output.append(classes_class.get_classes_by_class_id(course_id,cl))

        print(output)

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

<<<<<<< Updated upstream
@app.route("/learnerbadges", methods=['POST'])
def get_completed_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner_badges = learnerbadges()
    record = learner_badges.get_completed_courses(user_id)
=======
@app.route("/completed_courses", methods=['POST'])
def get_completed_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_completed_courses(user_id)
>>>>>>> Stashed changes
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
            "message": "There are no completed courses."
            }
        ), 404

@app.route("/get_all_learner_id",methods = ['GET'])
def get_all_learner_ids():
    lrnr = Learner()
    records = lrnr.get_all_learners_id()
    return records

@app.route("/get_all_learners",methods = ['GET'])
def get_all_learner():
    lrnr = Learner()
    record = lrnr.get_all_learners()
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

@app.route("/get_courses_with_classes_without_trainer",methods = ['GET'])
def get_courses_with_classes_without_trainer():
    record = ViewController.get_courses_with_classes_without_trainer()
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
            "message": "There are no classes without a trainer"
            }
        ), 404

@app.route("/get_classes_of_a_course_without_trainer",methods = ['POST'])
def get_classes_of_a_course_without_trainer():
    application = request.get_json()
    # print(application)
    c_id = application['course_id']
    
    record = ViewController.get_classes_of_a_course_without_trainer(c_id)
    
    # return record
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
            "message": "There are no classes without a trainer"
            }
        ), 404

@app.route("/get_all_trainers",methods = ['GET'])
def get_all_trainers():
    trnr = Trainer()
    
    record = trnr.get_all_trainers()
    
    # return record
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
            "message": "There are no classes without a trainer"
            }
        ), 404


if __name__ == '__main__':
    app.run(port=5002, debug=True)
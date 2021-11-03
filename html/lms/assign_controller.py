from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.functions import user
from trainer import Trainer_Assignment, Trainer
from employee_data_access import EmployeeDataAccess
from course import Course
from user import User
from learner import Learner, Learner_Assignment
from course_enrollment import Course_Enrollment
from learner_assignment import Learner_Assignment


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

CORS(app)

class AssignController():
    def assign_trainer(self,course_id,class_id,hr_id,trainer_id):

        usr = User()
        trnr = Trainer()

        valid_hr = usr.is_hr(hr_id)

        valid_trnr = trnr.is_trainer(trainer_id)

        course_to_assign = request.get_json()
        print("Request to assign course to user is received")

        if valid_hr and valid_trnr:
            #return assignment of course

            print("HR is assigning a class of a course to a trainer")

            userid = course_to_assign['trainer_id']
            course_id = course_to_assign['course_id']
            class_id = course_to_assign['class_id']

            trainer_assignement_entry = Trainer_Assignment(course_id = course_id, class_id = class_id,userid = userid)

            return trainer_assignement_entry.assign_class()
        
        else:
            #reject user from assigning courses
            return jsonify(
                {
                    "code": 404,
                    "message": "You either have no permission as a HR or the assigned user is not a trainer"
                }
            ), 404

    def get_assignment_trainer(self,userid):

        trnr = Trainer()
        
        if trnr:

            print("Retrieving Trainer ", userid , "'s assigned classes")
            return trnr.get_assigned_classes(userid)
            
        else:
            #reject user from retrieving
            return jsonify(
                {
                    "code": 404,
                    "message": "user id does not belong to a valid Trainer"
                }
            ), 404

    def assign_learner(self,course_id,class_id,hr_id,learner_id):

        usr = User()

        lrnr = Learner()

        valid_hr = usr.is_hr(hr_id)
        valid_lrnr = lrnr.is_learner(learner_id)

        class_to_assign = request.get_json()

        if valid_hr and valid_lrnr:

            print("HR is assigning and enrolling learner to a class of a course")


            userid = class_to_assign['learner_id']
            course_id = class_to_assign['course_id']
            class_id = class_to_assign['class_id']

            course_enrollment_entry = Learner_Assignment(course_id = course_id, userid = userid, class_id = class_id)

            return course_enrollment_entry.assign_class()
    
    




@app.route("/assign_course_trainer", methods=['POST'])
def assign_course_trainer():
    # if request.is_json():
    #     try:

    application = request.get_json(force=True)
    print(application)
    
    course_id = application['course_id']
    class_id = application['class_id']

    hr_id = application['hr_id']
    trainer_id = application['trainer_id']
    assign_ctrl = AssignController()
    return assign_ctrl.assign_trainer(course_id,class_id,hr_id,trainer_id)

@app.route("/get_assigned_courses",methods = ['POST'])
def get_assigned_classes_trainer():
    application = request.get_json(force=True)
    userid = application['userid']
    assign_ctrl = AssignController()
    return assign_ctrl.get_assignment_trainer(userid)

@app.route("/assign_course_learner", methods= ['POST'])
def assign_course_learner():
    application = request.get_json(force=True)
    course_id = application['course_id']
    class_id = application['class_id']
    hr_id = application['hr_id']
    learner_id = application['learner_id']
    assign_ctrl = AssignController()
    return assign_ctrl.assign_learner(course_id,class_id,hr_id,learner_id)

@app.route('/delete_assigned_classes', methods = ['POST'])
def delete_assigned_classes():
    application = request.get_json(force=True)
    course_id = application['course_id']
    class_id = application['class_id']
    user_id = application['user_id']

    lrnr_as_class = Learner_Assignment()
    return lrnr_as_class.delete_learner_assignment(course_id,class_id,user_id)


if __name__ == '__main__':
    app.run(port=5001, debug=True)

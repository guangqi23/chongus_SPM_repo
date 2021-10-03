from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from employee_data_access import EmployeeDataAccess
from course_class_data_access import CourseClassDataAccess

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class CourseController():
    def create_course(self, user_id):
        employee_da = EmployeeDataAccess()
        application = request.get_json()
        print("Request to create a course received")

        # call validate_hr in employee data access class
        valid_hr = employee_da.validate_hr(user_id)

        if valid_hr: # boolean return
            print("HR is requesting to create a new course")
            

            course_class_da = CourseClassDataAccess()
            status = course_class_da.create_course_record(application)

            return status

@app.route("/create_course", methods=['POST'])
def create_course():
    # if request.is_json():
    #     try:
    application = request.get_json()
    user_id = application['user_id']
    ctrl = CourseController()
    return ctrl.create_course(user_id)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
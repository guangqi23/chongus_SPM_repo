from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from employee_data_access import EmployeeDataAccess
from course import Course
from course_prerequisites import Course_Prerequisites

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class CourseController():
    def create_course(self, user_id, application):
        employee_da = EmployeeDataAccess()
        print("Request to create a course received")

        # call validate_hr in employee data access class
        valid_hr = employee_da.validate_hr(user_id)

        if valid_hr: # boolean return
            print("HR is requesting to create a new course")
            course_name = application["course_name"]
            course_description = application["course_description"]
            start_date = application["start_date"]
            end_date = application["end_date"]
            start_enrollment_date = application["start_enrollment_date"]
            end_enrollment_date = application["end_enrollment_date"]

            # check that all fields are not empty
            if all(field is not None for field in [course_name, course_description, start_date, end_date, start_enrollment_date, end_enrollment_date]):
                course_entry = Course(course_name=course_name, course_description=course_description, startdate=start_date, enddate=end_date, startenrollmentdate=start_enrollment_date, endenrollmentdate=end_enrollment_date)
                
                return course_entry.add_course()

            else:
                return jsonify(
                    {
                        "code": 400,
                        "message": "There are some fields that are empty"
                    }
                ), 400
            
    def delete_course(self, user_id):
        employee_da = EmployeeDataAccess()
        application = request.get_json()
        print("Request to create a course received")

        # call validate_hr in employee data access class
        valid_hr = employee_da.validate_hr(user_id)
        if valid_hr:
            print("HR is requesting to delete an existing course")
            course_id = application["course_id"]
            course_entry = Course()
            return course_entry.del_course(course_id)

    def create_prerequisites(self, user_id, course_id, application):
        employee_da = EmployeeDataAccess()
        course = Course()
        print("Request to create a course received")

        # call validate_hr in employee data access class
        valid_hr = employee_da.validate_hr(user_id)
        # check if the course exists on the database
        valid_course = course.get_course_by_id(course_id)

        if valid_hr and valid_course: # boolean return
            print("HR is requesting to add prerequisites to a course")
            prerequisites = application["prerequisites"]
            for prerequisite in prerequisites:
                # need to check if the prerequisite course exists in the database
                prereq = Course_Prerequisites(course_id=course_id, prereq_course_id=prerequisite)
                status = prereq.add_prerequisites()
                print(status)
                if status == 500:
                    return status
        
                # perform a check if prerequisites already existed and store them in an array
                # if the prerequisite is not a duplicate, store it in a separate array

            # later on this will return which prerequisites were duplicates and which were added as new prerequisites
            return status



# front end request
@app.route("/create_course", methods=['POST'])
def create_course():
    # if request.is_json():
    #     try:
    application = request.get_json()
    user_id = application['user_id']
    course_ctrl = CourseController()
    return course_ctrl.create_course(user_id,application)

@app.route("/delete_course", methods=['POST'])
def delete_course():
    # if request.is_json():
    #     try:
    application = request.get_json()
    user_id = application['user_id']
    course_ctrl = CourseController()
    return course_ctrl.delete_course(user_id)

@app.route("/courses", methods=['GET'])
def get_courses():
    courses = Course()
    record =  courses.get_all_courses()
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

@app.route("/add_prerequisites", methods=["POST"])
def create_prerequisites():
    application = request.get_json()
    course_id = application['course_id']
    user_id = application['user_id']
    course_ctrl = CourseController()
    return course_ctrl.create_prerequisites(user_id, course_id, application)

@app.route("/prerequisitesbycourse", methods=['POST'])
def prereq_by_course():
    application = request.get_json()
    print(request)
    course_id = application['course_id']
    prereq = Course_Prerequisites()
    record = prereq.prereq_by_course(course_id)
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
                "message": "There are no prerequisites."
            }
        ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)

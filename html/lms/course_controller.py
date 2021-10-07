from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from employee_data_access import EmployeeDataAccess
from course import Course, Course_Prerequisites

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
            course_id = application["course_id"]
            course_name = application["course_name"]
            course_description = application["course_description"]
            start_date = application["start_date"]
            end_date = application["end_date"]
            start_enrollment_date = application["start_enrollment_date"]
            end_enrollment_date = application["end_enrollment_date"]
            prerequisites = application["prerequisites"]

            # check that all fields are not empty
            if all(field is not None for field in [course_id, course_name, course_description, start_date, end_date, start_enrollment_date, end_enrollment_date, prerequisites]):
                course_entry = Course(course_id=course_id, course_name=course_name, course_description=course_description, startdate=start_date, enddate=end_date, startenrollmentdate=start_enrollment_date, endenrollmentdate=end_enrollment_date)

                for prerequisite in prerequisites:
                    prereq = Course_Prerequisites(course_id, prerequisite)
                    course_entry.add_prerequisites(prereq)
                    status = prereq.add_prereq()
                    print(status["message"])
                
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


# front end request
@app.route("/create_course", methods=['POST'])
def create_course():
    # if request.is_json():
    #     try:
    application = request.get_json()
    user_id = application['user_id']
    course_ctrl = CourseController()
    return course_ctrl.create_course(user_id)

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
    return courses.get_all_courses()
        
if __name__ == '__main__':
    app.run(port=5000, debug=True)
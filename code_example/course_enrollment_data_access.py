from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from course_enrollment import course_enrollment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class CourseEnrollmentDataAccess:
    
    def retrieveAllEnrollments(self):
        courseEnrollment = course_enrollment()
        enrollmentRecords = courseEnrollment.get_all_enrollments()
        print("Request to retrieve all enrollments received")
        return enrollmentRecords
        # call validate_hr in employee data access class
    
    def changeEnrollmentStatus(self, enrollment_id):
        courseEnrollment = course_enrollment()
        output = courseEnrollment.set_enrollment_status(enrollment_id)
        return output


# @app.route("/")
# def home():
#     return "Welcome!"


# @app.route("/retrieveAllEnrollments", methods=['GET'])
# def retrieveAllEnrollments():
#     a = CourseEnrollmentDataAccess()
#     output = a.retrieveAllEnrollments()
#     print(output)
#     return output

# @app.route("/changeEnrollmentStatus/input")
# def changeEnrollmentStatus():
#     enrollment_id = int(request.args.get('enrol_id', None))
#     a = CourseEnrollmentDataAccess()
#     result = a.changeEnrollmentStatus(enrollment_id)
#     return result


# if __name__ == '__main__':
#     app.run(port=5004, debug=True)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from course import Course

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class CourseClassDataAccess():
    def create_course_record(self, application):
        course_name = application["course_name"]
        course_description = application["course_description"]
        start_date = application["start_date"]
        end_date = application["end_date"]
        start_enrollment_date = application["start_enrollment_date"]
        end_enrollment_date = application["end_enrollment_date"]

        course_entry = Course(course_name=course_name, course_description=course_description, start_date=start_date, end_date=end_date, start_enrollment_date=start_enrollment_date, end_enrollment_date=end_enrollment_date)

        try: 
            db.session.add(course_entry)
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while creating the course. " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The course has been successfully created"
            }
        ), 200
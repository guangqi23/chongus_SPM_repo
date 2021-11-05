from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from classes import Classes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

# flask implementation
class Course(db.Model):
    __tablename__ = 'COURSE'

    # this is equivalent to the __init__ statement for classes but a flask implementation of it
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.String(300), nullable=False)
    startenrollmentdate = db.Column(db.DateTime, nullable=False)
    endenrollmentdate = db.Column(db.DateTime, nullable=False)

    def get_all_courses(self):
        return Course.query.all()

    def get_course_by_id(self, course_id):
        record = Course.query.filter_by(course_id=course_id).first()
        return record

    def add_course(self):
        # this should check if there is already an existing course in the database. To be added later
        try: 
            db.session.add(self)
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
    
    # def get_course_name(self):
    #     return self.course_name

    def del_course(self, course_id):
        course = self.query.filter_by(course_id=course_id).first()
        try: 
            db.session.delete(course)
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while deleting the course. " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The course has been successfully deleted"
            }
        ), 200
    
    def get_vacancies_by_courses(self, course_id):
        vacant_classes = Classes()
        class_by_course = vacant_classes.get_classes_by_course(course_id)
        course_vacancies = 0

        for a_class in class_by_course:
            course_vacancies += a_class.slots
        
        return course_vacancies

    def change_start_end_date(self, course_id, start_date, end_date):
        record = Course.query.filter_by(course_id = course_id)
        record.startenrollmentdate = start_date
        record.endenrollmentdate = end_date
        try:
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "A database error occured while changing the start and end date of the course " + str(error)
                }
            ), 500

        return jsonify (
                {
                    "code": 200,
                    "message": "The start and end date of the course has been successfully changed"
                }
            ), 200
        
   
    def json(self):
        return {"course_id": self.course_id, "course_name": self.course_name, "course_description": self.course_description, "startenrollmentdate": self.startenrollmentdate, "endenrollmentdate": self.endenrollmentdate}   


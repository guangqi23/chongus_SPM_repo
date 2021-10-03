from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

# flask implementation
class Course(db.Model):
    __tablename__ = 'course'

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.String(300), nullable=False)
    startdate = db.Column(db.DateTime, nullable=False)
    enddate = db.Column(db.DateTime, nullable=False)
    startenrollmentdate = db.Column(db.DateTime, nullable=False)
    endenrollmentdate = db.Column(db.DateTime, nullable=False)

    def __init__(self, course_name, course_description, start_date, end_date, start_enrollment_date, end_enrollment_date):
        self.course_name = course_name
        self.course_description = course_description
        self.startdate = start_date
        self.enddate = end_date
        self.startenrollmentdate = start_enrollment_date
        self.endenrollmentdate = end_enrollment_date

    def get_record_by_id(course_id):
        record = Course.query.filter_by(course_id=course_id).first()
        return record
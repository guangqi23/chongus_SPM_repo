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

    # this is equivalent to the __init__ statement for classes but a flask implementation of it
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.String(300), nullable=False)
    startdate = db.Column(db.DateTime, nullable=False)
    enddate = db.Column(db.DateTime, nullable=False)
    startenrollmentdate = db.Column(db.DateTime, nullable=False)
    endenrollmentdate = db.Column(db.DateTime, nullable=False)

    def get_record_by_id(self, course_id):
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
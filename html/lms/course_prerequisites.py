from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class Course_Prerequisites(db.Model):
    __tablename__ = 'course_prerequisite'

    course_id = db.Column(db.Integer, primary_key=True)
    prereq_course_id = db.Column(db.Integer, primary_key=True)

    def add_prerequisites(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            return jsonify(
                {
                    "code": 500,
                    "message": "There was an error when adding the prerequisite. " + str(error)
                }
            ), 500
        
        return jsonify(
            {
                "code": 200,
                "message": "The prerequisite has been successfully added"
            }
        ), 200

    def prereq_by_course(self,course_id):
        record = Course_Prerequisites.query.filter_by(course_id=course_id).all()
        return record

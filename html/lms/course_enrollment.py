from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.sqltypes import Boolean
from user import User
# from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy import Column, Integer

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Course_Enrollment(db.Model):

    __tablename__ = 'COURSE_ENROLLMENT'

    enrollment_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, nullable = False)    
    userid = db.Column(db.Integer, nullable = False)
    class_id = db.Column(db.Integer, nullable = False)
    is_enrolled = db.Column(db.Boolean, nullable = False)

    def add_enrollment_record(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while assigning the class to learner " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "Learner has succesfully enrolled into a class by HR"
            }
        ), 200
    
    def delete_enrollment_record(self, user_id, class_id, course_id):
        enrollment_record = self.query.filter_by(userid = user_id, class_id = class_id, course_id = course_id).first()
        try:
            db.session.delete(enrollment_record)
            db.session.commit()
        except Exception as error:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occured while deleting the enrollment record. " + str(error)
                }
            )

        return jsonify(
            {
                "code": 200,
                "message": "The enrollment record has been successfully deleted"
            }
        ), 200

    def get_user_enrolled_courses(self, userid):
        record = Course_Enrollment.query.filter_by(userid=userid).all()
        return record
    
    def json(self):
        return {"enrollment_id":self.enrollment_id,"course_id":self.course_id,"userid":self.userid, "class_id":self.class_id, "is_enrolled":self.is_enrolled }

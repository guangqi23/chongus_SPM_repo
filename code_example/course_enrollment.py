from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app) 

class course_enrollment(db.Model):
    __tablename__ = 'COURSE_ENROLLMENT'
    enrollment_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    is_enrolled = db.Column(db.Boolean)
    
    def json(self):
        return {"enrollment_id": self.enrollment_id,"course_id": self.course_id,"userid": self.userid, "class_id": self.class_id, "is_enrolled": self.is_enrolled}

    def get_enrollment_id(self):
        return self.enrollment_id
        
    def get_course_id(self):
        return self.course_id

    def get_userid(self):
        return self.userid

    def get_class_id(self):
        return self.class_id

    def get_enrollment_status(self):
        return self.is_enrolled

    def get_all_enrollments(self):
        all_enrollments = course_enrollment.query.all()
        if len(all_enrollments):
            return jsonify(
                {
                    "code":200,
                    "data": {
                        "enrollment_records" : [records.json() for records in all_enrollments]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There is no enrollment records!"
            }
        ),404


    def set_enrollment_status(self,selectedEnrollId):
        courseEnrollRecord = course_enrollment.query.filter_by(enrollment_id = selectedEnrollId).first()
        if courseEnrollRecord.is_enrolled == False:
            courseEnrollRecord.is_enrolled = True
            db.session.commit()
            return "Changed enrollment status to True!"
        else:
            courseEnrollRecord.is_enrolled = False
            db.session.commit()
            return "Changed enrollment status to False!"
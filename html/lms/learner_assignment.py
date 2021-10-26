from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import false, true

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class Learner_Assignment(db.Model):
    __tablename__ = 'LEARNERASSIGNMENT'

    course_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, primary_key=True, index=True)
    userid = db.Column(db.Integer, primary_key=True, index=True)

    def get_user_assigned_courses(self, userid): 
        record = Learner_Assignment.query.filter_by(userid=userid).all()
        return record
    
    def json(self):
        return {"course_id":self.course_id,"class_id":self.class_id, "userid":self.userid}

    def assign_class(self):

        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while assigning the class " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The class has been successfully assigned to the Learner"
            }
        ), 200
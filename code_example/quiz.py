from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from finalquiz import FinalQuiz
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app) 

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    quiz_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer)
    time_limit = db.Column(db.Integer)
    

    def json(self):
        return {"quiz_id": self.quiz_id,"section_id": self.section_id, "time_limit": self.time_limit}

    def get_quiz_id(self):
        return self.quiz_id

    def get_section_id(self):
        return self.section_id

    def get_time_limit(self):
        return self.time_limit

    def get_quiz(self,section_id):
        quizzes = Quiz.query.filter_by(section_id=section_id).first()
        return jsonify(
            {
                "code": 200,
                "data": quizzes.json()
            })
        return jsonify(
            {
                "code": 404,
                "message": "There are no quiz."
            }
        )


        
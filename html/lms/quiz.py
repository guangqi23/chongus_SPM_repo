from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from finalquiz import FinalQuiz
from quiz_question import QuizQuestions
from sqlalchemy import desc
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app) 

class Quiz(db.Model):
    __tablename__ = 'QUIZZES'
    quiz_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer)
    time_limit = db.Column(db.Integer)
    

    def json(self):
        return {"quiz_id": self.quiz_id,"section_id": self.section_id, "time_limit": self.time_limit}

    def get_quiz_id(self):
        return self.quiz_id

    def get_section_id(self):
        return self.section_id

    def get_time_limit_with_id(self, quiz_id_input):
        quizObj = Quiz.query.filter_by(quiz_id= quiz_id_input).first()
        timer = quizObj.time_limit
        db.session.close()
        return str(timer)

    def get_section_id_with_quiz_id(self, quiz_id):
        quizObj = Quiz.query.filter_by(quiz_id= quiz_id).first()
        section_id = quizObj.section_id
        db.session.close()
        return section_id

    def get_quiz(self,section_id):
        qid = self.quiz_id
        quizzes = Quiz.query.filter_by(section_id=section_id)
        #get last value
        db.session.close()
        last_id = quizzes[-1]
        return jsonify(
            {
                "code": 200,
                "data": last_id.json()
            })
        
    def add_questions(self,questions):
        self.question.append(questions)

    def get_quiz_by_id(self,quiz_id):
        quizzes = Quiz.query.filter_by(quiz_id=quiz_id).first()
       
        db.session.close()
      
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
   


        
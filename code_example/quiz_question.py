from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app) 

class QuizQuestions(db.Model):
    __tablename__ = 'quiz_question'
    question_id= db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer)
    qorder = db.Column(db.Integer)
    question_type = db.Column(db.String(100))
    question = db.Column(db.String(500))
    def json(self):
        return {"question_id": self.quiz_id,"quiz_id": self.quiz_id, "qorder": self.qorder,"question_type": self.question_type,"question": self.question }

    def get_quiz_id(self):
        return self.quiz_id

    def get_question_id(self):
        return self.question_id

    def get_question_type(self):
        return self.question_type
    
    def get_qorder(self):
        return self.qorder

    def get_question(self):
        return self.question

    def get_quiz_questions(self,quiz_id):
        questions = QuizQuestions.query.filter_by(quiz_id = quiz_id)
        #check if empty
        count =0
        for x in questions:
            count+=1

        if count!=0:
            return jsonify(
                {
                    "code": 200,
                    "data": [question.json() for question in questions]
                })
        return jsonify(
            {
                "code": 404,
                "message": "There are no section."
            }
        )
        
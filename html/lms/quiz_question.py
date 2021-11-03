from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app) 

class QuizQuestions(db.Model):
    __tablename__ = 'QUIZ_QUESTION'
    question_id= db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer)
    qorder = db.Column(db.Integer)
    question_type = db.Column(db.String(100))
    question = db.Column(db.String(500))
    __mapper_args__ ={
        'polymorphic_identity': question_type
    }

    def json(self):
        return {"question_id": self.question_id,"quiz_id": self.quiz_id, "qorder": self.qorder,"question_type": self.question_type,"question": self.question }

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

    


        
class TrueFalse(QuizQuestions):
    __tablename__ = 'TRUEFALSEQ'
    
    question_id = db.Column(db.Integer, db.ForeignKey('QUIZ_QUESTION.question_id'), primary_key=True)
    answer = db.Column(db.Boolean)
    __mapper_args__ = {'polymorphic_identity': 'TF','inherit_condition': (question_id == QuizQuestions.question_id)}
    
    def json(self):
        return {"answer":self.answer,"question_id": self.question_id,"quiz_id": self.quiz_id, "qorder": self.qorder,"question_type": self.question_type,"question": self.question }
        
    def get_question_id(self):
        return self.question_id


    def get_answer(self):
        return self.answer

    def get_true_false_options(self,question_id):
        tf = TrueFalse.query.filter_by(question_id=question_id).first()
        db.session.close()
        return tf

    def get_quiz_questions(self,question_id):
        questions = TrueFalse.query.filter_by(question_id =question_id)
        #check if empty
        y = self.get_qorder()
        count =0
        db.session.close()
        for x in questions:
            count+=1

        if count!=0:
            return jsonify(
                {
                    
                    "data": [question.json() for question in questions]
                })
        return jsonify(
            {
                "code": 404,
                "message": "There are no section."
            }
        )


class multiplechoice(QuizQuestions):
    __tablename__ = 'MCQ'
    question_id= db.Column(db.Integer,db.ForeignKey('QUIZ_QUESTION.question_id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'MCQ','inherit_condition': (question_id == QuizQuestions.question_id)}

    def json(self):
        return {"question_id": self.question_id,"quiz_id": self.quiz_id, "qorder": self.qorder,"question_type": self.question_type,"question": self.question }
'''
class multiplechoiceoptions(db.Model):
    _tablename__ = 'mcq_options'
    question_id= db.Column(db.Integer, primary_key=True)
    option_order = db.Column(db.Integer,primary_key=True)
    correct_option = db.Column(db.Boolean, nullable=False)
    option_content = db.Column(db.String(100))
    
    def json(self):
        return {"question_id": self.question_id,"option_order": self.option_order,"option_content": self.option_content,"correct_option": self.correct_option,"question_id":self.question_id}
        
    def get_question_id(self):
        return self.question_id

    def get_option_order(self):
        return self.option_order

    def get_option_content(self):
        return self.option_content

    def correct_option(self):
        return self.correct_option
        
    def get_quiz(self,question_id):
        option= multiplechoiceoptions.query.filter_by(question_id = question_id)
       
        count =0
        for x in option:
            count+=1
        if count!=0:
            return jsonify(
                {
                    
                    "data": [question.json() for question in option]
                })
        return jsonify(
            {
                "code": 404,
                "message": "There are no section."
            }
        )
       
'''
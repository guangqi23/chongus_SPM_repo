from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app) 

class TrueFalse(db.Model):
    __tablename__ = 'truefalseq'
    question_id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Boolean)

    
    def json(self):
        return {"question_id": self.question_id,"answer": self.answer}
        
    def get_question_id(self):
        return self.question_id


    def get_answer(self):
        return self.answer

    def get_true_false_options(self,question_id):
        tf = TrueFalse.query.filter_by(question_id=question_id).first()
        return tf
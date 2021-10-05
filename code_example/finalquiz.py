from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app) 

class FinalQuiz(db.Model):
    __tablename__ = 'final_quiz'
    quiz_id = db.Column(db.Integer, primary_key=True)
    passing_score = db.Column(db.Integer)

    
    def json(self):
        return {"quiz_id": self.quiz_id,"passing_score": self.passing_score}
        
    def get_quiz_id(self):
        return self.quiz_id

    def get_passing_score(self):
        return self.passing_score

    def get_quiz(self,quiz_id):
        section = FinalQuiz.query.filter_by(quiz_id = quiz_id).first()
        return section
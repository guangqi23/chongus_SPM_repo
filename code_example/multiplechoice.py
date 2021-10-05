from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app) 

class multiplechoice(db.Model):
    __tablename__ = 'mcq_options'
    question_id= db.Column(db.Integer, primary_key=True)
    option_order = db.Column(db.Integer,primary_key=True)
    option_content = db.Column(db.String(100))
    correct_option = db.Column(db.Boolean)
    

    
    def json(self):
        return {"question_id": self.question_id,"option_order": self.option_order,"option_content": self.option_content,"correct_option": self.correct_option}
        
    def get_question_id(self):
        return self.question_id

    def get_option_order(self):
        return self.option_order

    def get_option_content(self):
        return self.option_content

    def correct_option(self):
        return self.correct_option
        
    def get_quiz(self,quiz_id):
        option= multiplechoice.query.filter_by(quiz_id = quiz_id)
        return option
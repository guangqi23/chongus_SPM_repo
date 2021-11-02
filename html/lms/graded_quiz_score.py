from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = model.db
db = SQLAlchemy(app)

CORS(app) 

class Graded_quiz_score(db.Model):
    __tablename__ = 'GRADED_QUIZ_SCORE'

    userid = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_score = db.Column(db.Float, nullable=True)
    result = db.Column(db.Boolean, nullable = True)
    time_inserted = db.Column(db.DateTime, primary_key = True)


    def json(self):
        return {"user_id": self.userid, "quiz_id": self.quiz_id, "quiz_score": self.quiz_score, "result": self.result, "time_inserted" : datetime.now()}

    def insert_score(self, scoreObj): 
        
        scoreRecord = Graded_quiz_score(userid = scoreObj['user_id'], quiz_id = scoreObj['quiz_id'], quiz_score = scoreObj['quiz_score'], result = scoreObj['result'], time_inserted = datetime.now())
        db.session.add(scoreRecord)
        db.session.commit()
        db.session.close()
        return "Success"
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

<<<<<<< Updated upstream
class learnerbadges(db.Model):
    __tablename__ = 'LEARNER_BADGES'
=======
class Learner_Badges(db.Model):
    __tablename__ = 'learner_badges'
>>>>>>> Stashed changes

    userid = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, primary_key=True)

    def json(self):
        return {"user_id": self.userid, "course_id": self.course_id}

    def get_learner_badges(self, userid):
        record = self.query.filter_by(userid=userid).all()
        return record


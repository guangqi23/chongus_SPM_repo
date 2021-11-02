from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = models.db

CORS(app) 

# flask implementation
class User(db.Model):
    __tablename__ = 'USERS'
    __mapper_args__ = {
        'polymorphic_identity':'user'
    }

    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)

    # def __init__(self, user_id, name, email, department, designation):
    #     self.user_id = user_id
    #     self.name = name
    #     self.email = email
    #     self.department = department
    #     self.designation = designation

    def json(self):
        return {"user_id": self.userid, "name": self.name, "email": self.email, "department": self.department, "designation": self.designation}

    def get_name(self):
        return self.name

    def get_user_id(self):
        return self.userid

    def is_hr(self, userid):
        user = User.query.filter_by(userid=userid).first()
        return user

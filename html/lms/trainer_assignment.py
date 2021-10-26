from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from user import User
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy import Column, Integer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class Trainer_Assignment(db.Model):
    __tablename__ = 'TRAINERASSIGNMENT'

    
    
    course_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, primary_key=True, index=True)
    userid = db.Column(db.Integer, primary_key=True, index=True)

  
    # guang never do boooooo
    # def get_assigned_classes(self):
        
    #     classes = Trainer_Assignment.query.filter_by(userid=self.userid)

    #     return classes
    #     return_assigned = []

    #     ##incomplete
    
    def get_course_id(self):
        return self.course_id
    
    def get_class_id(self):
        return self.class_id
    
    def get_user_id(self):
        return self.userid
    
    def get_all_trainer_assignments(self):
        return Trainer_Assignment.query.all()

    def assign_class(self):

        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while assigning the class " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The class has been successfully assigned to the trainer"
            }
        ), 200
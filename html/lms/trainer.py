from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from user import User
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy import Column, Integer
from trainer_assignment import Trainer_Assignment

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class Trainer(User):
    __tablename__ = 'TRAINERS'

    __mapper_args__ = {'polymorphic_identity': 'trainer'}
    
    def is_trainer(self, userid):
        trnr = Trainer.query.filter_by(userid=userid).first()
        return trnr

    def get_user_id(self):
        return self.userid
    
    def get_all_trainers(self):
        trnr = Trainer()
        return trnr.query.filter_by(designation='Trainer').all()

    def get_assigned_classes(self,userid):
        
        classes = Trainer_Assignment.query.filter_by(userid=userid)

        results_dict = {}
        count = 1   
        for eachClass in classes:
            
            msg = "class " + str(count)
            u_id = eachClass.get_user_id()
            co_id = eachClass.get_course_id()
            cla_id = eachClass.get_class_id()
            results_dict[msg] = {'course_id' : co_id, "class_id" : cla_id , "userid" : u_id}
            count+=1

        return results_dict
      




    
    
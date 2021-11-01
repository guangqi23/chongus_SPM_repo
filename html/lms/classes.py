from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Classes(db.Model):
    __tablename__ = 'CLASSES'

    class_id = db.Column(db.Integer, primary_key=True)
    course_id= db.Column(db.Integer)
    slots = db.Column(db.Integer)
    startdate = db.Column(db.DateTime)
    enddate = db.Column(db.DateTime)
    trainer_name = db.Column(db.String(64))

    def init(self, course_id, class_id, slots, start_date, end_date, trainer_name):
        self.course_id = course_id
        self.class_id = class_id
        self.slots = slots
        self.startdate = start_date
        self.enddate = end_date
        self.trainer_name = trainer_name
    

    def getSlots(self, cid):
        slots = Classes.query.filter_by(class_id = cid).first()
        return str(slots.slots)

    def get_classes_by_class_id(self,course_id,class_id):
        record = Classes.query.filter_by(class_id=class_id,course_id=course_id).first()
        return record
    
    def get_classes_by_course(self, course_id):
        record = Classes.query.filter_by(course_id=course_id).all()
        return record

    #By Xing Jie 
    def get_class_startdate(self, class_id):
        class_A = Classes.query.filter_by(class_id = class_id).first()
        return str(class_A.startdate)

    def json(self):
        return {"class_id":self.class_id,"course_id":self.course_id,"slots":self.slots,"startdate":self.startdate, "enddate":self.enddate, "trainer_name": self.trainer_name}
    
    
    

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json


app = Flask(name)
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Classes(db.Model):
    tablename = 'CLASSES'

    class_id = db.Column(db.Integer, primary_key=True)
    course_id= db.Column(db.Integer)
    slots = db.Column(db.Integer)


    def init(self, course_id, class_id, slots):
        self.course_id = course_id
        self.class_id = class_id
        self.slots = slots
    
    def getSlots(cid):
        slots = Classes.query.filter_by(class_id = cid).first()
        return str(slots.slots)

    def json(self):
        return {"class_id":self.class_id,"course_id":self.course_id,"slots":self.slots}
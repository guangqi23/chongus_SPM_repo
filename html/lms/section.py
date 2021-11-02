from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sectionmaterials import SectionMaterials

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app) 

class Section(db.Model):
    __tablename__ = 'SECTIONS'
    section_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    section_title = db.Column(db.String(500))
    

    def json(self):
        return {"section_id": self.section_id, "class_id": self.class_id,"section_title": self.section_title}

    def get_class_id(self):
        return self.class_id

    def get_section_id(self):
        return self.section_id

    def get_section_title(self):
        return self.section_title

    def get_section_title_with_id(self, sect_id):
        section = Section.query.filter_by(section_id= sect_id).first()
        section_title = section.section_title
        return section_title

    def get_sections(self, section_id):
        section = Section.query.filter_by(section_id=section_id).first()
        return section

    def get_section_all(self,class_id):
        sections  = Section.query.filter_by(class_id=class_id)
        #check if empty
        count =0
        for x in sections:
            count+=1

        if count!=0:
            return jsonify(
                {
                    "code": 200,
                    "data": [section.json() for section in sections]
                })
        return jsonify(
            {
                "code": 404,
                "message": "There are no section."
            }
        )

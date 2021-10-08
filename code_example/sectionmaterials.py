from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app) 

class SectionMaterials(db.Model):
    __tablename__ = 'SECTIONS_MATERIALS'
    material_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer)
    material_title = db.Column(db.String(100), nullable=False)
    material_content =db.Column(db.String(500), nullable=False)
    material_type =db.Column(db.String(100), nullable=False)
    
    def json(self):
        return {"material_id": self.material_id,"section_id": self.section_id,"material_title":self.material_title, "material_content": self.material_content,"material_type":self.material_type}

    def get_material_id(self):
        return self.material_id

    def get_section_id(self):
        return self.section_id
    
    def get_section_material_title(self):
        return self.material_title

    def get_section_material_content(self):
        return self.material_content

    def get_section_material_type(self):
        return self.material_type

    def get_materials_individual(self, material_id,section_id):
        material= SectionMaterials.query.filter_by(section_id=section_id, material_id = material_id).first()
        return material

    def get_materials_all(self, section_id):
        materials  = SectionMaterials.query.filter_by(section_id=section_id)
        #check if empty
        count =0
        for x in materials:
            count+=1

        if count!=0:
            return jsonify(
                {
                    "code": 200,
                    "data": [material.json() for material in  materials]
                })
        return jsonify(
            {
                "code": 404,
                "message": "There are no materials in this section."
            }
        )
    

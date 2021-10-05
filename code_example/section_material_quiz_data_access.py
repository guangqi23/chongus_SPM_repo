from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sectionmaterials import SectionMaterials
from section import Section
from quiz import Quiz
from quiz_question import QuizQuestions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class SectionMaterialQuizDataAccess():
    def get_material_record_by_section(self, section_id):
        da = SectionMaterials()
        materials = da.get_materials_all(section_id)
        return materials
    
    def get_sections_by_class(self,class_id):
        da = Section()
        section = da.get_section_all(class_id)
        return section

    def get_section_quiz(self,section_id):
        da = Quiz()
        section = da.get_quiz(section_id)
        return section

    def get_quiz_questions(self,quiz_id):
        da = QuizQuestions()
        questions = da.get_quiz_questions(quiz_id)
        return questions

    def create_section(self,class_id,section_title):
        section_entry = Section(class_id = class_id,section_title=section_title)
        try: 
            db.session.add(section_entry)
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while creating the section. " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The section has been successfully created"
            }
        ), 200
    
    def create_quiz(self,section_id,time_limit):
        quiz_entry = Quiz(section_id = section_id,time_limit=time_limit)
        try: 
            db.session.add(quiz_entry)
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while creating the section. " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The section has been successfully created"
            }
        ), 200

    def create_material(self,section_id,material_title,material_content):
        material_entry = SectionMaterials(section_id=section_id,material_title=material_title,material_content=material_content)

        try: 
            db.session.add(material_entry)
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while creating the material. " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The material has been successfully created"
            }
        ), 200
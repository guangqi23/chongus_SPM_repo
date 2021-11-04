from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sectionmaterials import SectionMaterials
from section import Section
from quiz import Quiz

from quiz_question import QuizQuestions
from quiz_question import multiplechoice
from quiz_question import TrueFalse
from multiplechoiceoptions import multiplechoiceoptions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class SectionMaterialQuizDataAccess():
    def view_qn(self,quiz_id):
        da = TrueFalse()
        questions = da.get_quiz_questions(quiz_id)
        return questions
        

    def get_material_record_by_section(self, section_id):
        if section_id >0:
            da = SectionMaterials()
            materials = da.get_materials_all(section_id)
            return materials
        else:
            raise Exception ("Section Id must be above 0");
    
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
                "message": "The section has been successfully created",
                "quiz_id": quiz_entry.get_quiz_id()
            }
        ), 200

    def create_material(self,section_id,material_title,material_content,material_type):
        material_entry = SectionMaterials(section_id=section_id,material_title=material_title,material_content=material_content,material_type=material_type)

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

    def create_TrueFalse(self,answer,quiz_id,qorder,question_type,question):
        question_entry = TrueFalse(quiz_id = quiz_id, answer = answer, qorder = qorder, question_type = question_type, question=question)
        
        try: 
            db.session.add(question_entry)
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while creating the question. " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The question has been successfully created"
            }
        ), 200

    def create_MCQ(self,quiz_id,qorder,question_type,question):
        question_entry = QuizQuestions(quiz_id=quiz_id,question_type=question_type,qorder=qorder,question=question)
        try: 
            db.session.add(question_entry)
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while creating the question. " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The question has been successfully created",
                "id": question_entry.get_question_id()
            }
        ), 200

    def create_MCQ_options(self,question_id,option_order,option_content,correct_option):
        
        option_entry = multiplechoiceoptions(question_id = question_id,option_order =option_order,option_content = option_content,correct_option = correct_option)
        print('entry c-option is ',option_entry.get_correct_option())
        try: 
            db.session.add(option_entry)
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while creating the option. " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The option has been successfully created",
                "data":option_entry.json()
            }
        ), 200

    def get_TrueFalse(self,question_id):
        da = TrueFalse()
        questions = da.get_quiz_questions(question_id)
        return questions
    
    def get_MCQ(self,question_id):
        da = multiplechoiceoptions()
        questions = da.get_options_by_question_id(question_id)
        return questions

    def delete_Quiz(self,quiz_id):
        '''delete_quiz =QuizQuestions.query.filter_by(quiz_id = quiz_id).delete()
        delete_tf = TrueFalse.query.filter_by(quiz_id = quiz_id).delete()'''
        record_obj = db.session.query(TrueFalse).filter(TrueFalse.quiz_id== quiz_id)
        db.session.delete(record_obj)
        db.session.commit()
        '''
        try: 
            db.session.delete(delete_tf)
            db.session.delete(delete_quiz)
            db.session.commit()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while deleting the quiz. " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The questions has been successfully quiz",
                
            }
        ), 200'''
    def get_section_quiz_by_qid(self,quiz_id):
        da = Quiz()
        data = da.get_quiz_by_id(quiz_id)
        return data
    
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from  section_material_quiz_data_access import SectionMaterialQuizDataAccess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class SectionMaterialController():
    def create_materials(self, section_id):
        pass

#   View all materials in a section
    def view_all_materials(self,section_id):
        da = SectionMaterialQuizDataAccess()
        materials = da.get_material_record_by_section(section_id)
        return materials


#   View all sections in a class
    def view_all_sections(self, class_id):
        da = SectionMaterialQuizDataAccess()
        sections = da.get_sections_by_class(class_id)
        return sections
    
#   Get quiz id of that section
    def view_section_quiz(self,section_id):
        da = SectionMaterialQuizDataAccess()
        sections = da.get_section_quiz(section_id)
        return sections

#   Create section
    def create_section(self,class_id,section_title):
        da = SectionMaterialQuizDataAccess()
        status = da.create_section(class_id,section_title)
        return status

#   Create Quizzes
    def create_quiz(self,section_id,time_limit):
        da = SectionMaterialQuizDataAccess()
        status = da.create_quiz(section_id,time_limit)
        return status

#   View Quiz Questions
    def get_quiz_questions(self,quiz_id):
        da = SectionMaterialQuizDataAccess()
        questions = da.get_quiz_questions(quiz_id)
        return questions


#   Create Quiz Questions
    def create_quiz_questions(self, quiz_id,question_type,qorder,question):
        da = SectionMaterialQuizDataAccess()
        status = da.create_quiz(quiz_id,question_type,qorder,question)
        return status

#   Create Course Materials
    def create_section_materials(self,section_id,material_title,material_content,material_type):
        da = SectionMaterialQuizDataAccess()
        status = da.create_material(section_id,material_title,material_content,material_type)
        return status

    


#   Download Course Materials
    #tbu after initializing S3

        
@app.route("/create_materials", methods=['GET'])
def create_Materials(self):
    pass


############## View Functions ###############################
@app.route("/view_section_materials", methods=['GET'])
def view_Materials():
    section_id = int(request.args.get('section_id', None))
    da = SectionMaterialController()
    materials = da.view_all_materials(section_id)
    return materials

    
@app.route("/view_class_sections", methods=['GET'])
def view_Sections():
    class_id = int(request.args.get('class_id', None))
    da = SectionMaterialController()
    sections = da.view_all_sections(class_id)
    return sections

@app.route("/view_section_quiz", methods=['GET'])
def view_Quiz():
    section_id = int(request.args.get('section_id', None))
    da = SectionMaterialController()
    quiz = da.view_section_quiz(section_id)
    return quiz


@app.route("/create_section", methods=['GET'])
def create_section():
    class_id = int(request.args.get('class_id', None))
    section_title = str(request.args.get('section_title', None))
    da = SectionMaterialController()
    status = da.create_section(class_id,section_title)
    return status

@app.route("/create_quiz", methods=['GET'])
def create_quiz():
    section_id = int(request.args.get('section_id', None))
    time_limit = int(request.args.get('time_limit', None))
    da =SectionMaterialController()
    status = da.create_quiz(section_id,time_limit)
    return status
    
@app.route("/get_quiz_questions", methods=['GET'])
def get_quiz_questions():
    quiz_id = int(request.args.get('quiz_id', None))
    da = SectionMaterialController()
    status = da.get_quiz_questions(quiz_id)
    return status

@app.route("/create_quiz_questions", methods=['GET'])
def create_quiz_questions():
    quiz_id = int(request.args.get('quiz_id', None))
    question_type = str(request.args.get('quiz_id', None))
    qorder = str(request.args.get('qorder', None))
    question =str(request.args.get('question', None))
    da = SectionMaterialController()
    status = da.create_quiz_questions(quiz_id,question_type,qorder,question)
    return status


@app.route("/view_quiz_questions", methods=['GET'])
def get_qn():
    qn_id = int(request.args.get('qn_id', None))
    da =  SectionMaterialController()
    quiz = da.view_qn(qn_id)
    return quiz

@app.route("/create_section_materials", methods=['GET'])
def create_section_materials():
    section_id = int(request.args.get('section_id', None))
    material_title = str(request.args.get('material_title', None))
    material_content = str(request.args.get('material_content', None))
    material_type = str(request.args.get('material_type', None))
    da = SectionMaterialController()
    status = da.create_section_materials(section_id,material_title,material_content,material_type)
    return status




if __name__ == '__main__':
    app.run(port=5001, debug=True)
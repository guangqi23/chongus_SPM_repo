from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from  section_material_quiz_data_access import SectionMaterialQuizDataAccess

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class SectionQuizController():
    def create_materials(self, section_id):
        pass

#   View all materials in a section



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


#   Create Quizzes
    def create_quiz(self,section_id,time_limit):
        da = SectionMaterialQuizDataAccess()
        status = da.create_quiz(section_id,time_limit)
        return status


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
    def create_TrueFalse_qn(self,answer,quiz_id,qorder,question_type,question):
        da = SectionMaterialQuizDataAccess()
        status = da.create_TrueFalse(answer,quiz_id,qorder,question_type,question)
        return status

    def create_MCQ_qn(self,quiz_id,qorder,question_type,question):
        da = SectionMaterialQuizDataAccess()
        status = da.create_MCQ(quiz_id,qorder,question_type,question)
        return status
    
    def create_MCQ_options(self,question_id,option_order,option_content,correct_option):
        da = SectionMaterialQuizDataAccess()
        status = da.create_MCQ_options(question_id,option_order,option_content,correct_option)
        return status

        


############## View Functions ###############################
@app.route("/view_section_materials", methods=['GET'])
def view_Materials():
    section_id = int(request.args.get('section_id', None))
    da = SectionQuizController()
    materials = da.view_all_materials(section_id)
    return materials

    
@app.route("/view_class_sections", methods=['GET'])
def view_Sections():
    class_id = int(request.args.get('class_id', None))
    da = SectionQuizController()
    sections = da.view_all_sections(class_id)
    return sections

@app.route("/view_section_quiz", methods=['GET'])
def view_Quiz():
    section_id = int(request.args.get('section_id', None))
    da = SectionQuizController()
    quiz = da.view_section_quiz(section_id)
    return quiz


@app.route("/create_quiz", methods=['GET'])
def create_quiz():
    section_id = int(request.args.get('section_id', None))
    time_limit = int(request.args.get('time_limit', None))
    da = SectionQuizController()
    status = da.create_quiz(section_id,time_limit)
    return status
    
@app.route("/get_quiz_questions", methods=['GET'])
def get_quiz_questions():
    quiz_id = int(request.args.get('quiz_id', None))
    da = SectionQuizController()
    status = da.get_quiz_questions(quiz_id)
    return status

@app.route("/create_quiz_questions", methods=['GET'])
def create_quiz_questions():
    quiz_id = int(request.args.get('quiz_id', None))
    question_type = str(request.args.get('quiz_id', None))
    qorder = str(request.args.get('qorder', None))
    question =str(request.args.get('question', None))
    da = SectionQuizController()
    status = da.create_quiz_questions(quiz_id,question_type,qorder,question)
    return status


@app.route("/view_quiz_questions", methods=['GET'])
def get_qn():
    qn_id = int(request.args.get('qn_id', None))
    da =  SectionMaterialQuizDataAccess()
    quiz = da.view_qn(qn_id)
    return quiz

@app.route("/create_section_materials", methods=['GET'])
def create_section_materials():
    section_id = int(request.args.get('section_id', None))
    material_title = str(request.args.get('material_title', None))
    material_content = str(request.args.get('material_content', None))
    material_type = str(request.args.get('material_type', None))
    da = SectionQuizController()
    status = da.create_section_materials(section_id,material_title,material_content,material_type)
    return status

@app.route("/create_TrueFalse", methods=['GET', 'POST'])
def create_TrueFalse():
    answer = int(request.args.get('answer', None))
    quiz_id = int(request.args.get('quiz_id', None))
    qorder = int(request.args.get('qorder', None))
    question_type = str(request.args.get('question_type', None))
    question = str(request.args.get('question', None))
    print(answer)
    da = SectionQuizController()
    status = da.create_TrueFalse_qn(answer,quiz_id,qorder,question_type,question)
    return status

@app.route("/create_MCQ_Question", methods=['GET'])
def create_MCQ():
    quiz_id = int(request.args.get('quiz_id', None))
    qorder = int(request.args.get('qorder', None))
    question_type = str(request.args.get('question_type', None))
    question = str(request.args.get('question', None))
    da = SectionQuizController()
    status = da.create_MCQ_qn(quiz_id,qorder,question_type,question)
    return status

@app.route("/add_MCQ_Options", methods=['GET'])
def add_MCQ_options():
    question_id = int(request.args.get('question_id', None))
    option_order = int(request.args.get('option_order', None))
    option_content = str(request.args.get('option_content', None))
    correct_option = int(request.args.get('correct_option',None))
    print('controller option',correct_option)
    da = SectionQuizController()
    status = da.create_MCQ_options(question_id,option_order,option_content,correct_option)
    
    return status 



if __name__ == '__main__':
    app.run(port=5002, debug=True)
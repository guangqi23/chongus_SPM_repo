import sys
import requests

from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from sqlalchemy.sql.elements import Null

# from classes import Classes
# from course_enrollment import Course_Enrollment
# from course_prerequisites import Course_Prerequisites
# from course import Course
# from employee_data_access import EmployeeDataAccess
# from enrollment_controller import EnrollmentController
# from finalquiz import FinalQuiz
# from learner_assignment import Learner_Assignment
# from learner_badges import Learner_Badges
# from learner import Learner
# from multiplechoiceoptions import multiplechoiceoptions
# from quiz_question import QuizQuestions
# from quiz import Quiz
# from section_material_quiz_data_access import SectionMaterialQuizDataAccess
# from section import Section
# from sectionmaterials import SectionMaterials
# from trainer_assignment import Trainer_Assignment
# from trainer import Trainer
# from user import User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app, session_options={
    'expire_on_commit': False
})

CORS(app)

class User(db.Model):
    __tablename__ = 'USERS'
    __mapper_args__ = {
        'polymorphic_identity':'user'
    }

    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)

    # def __init__(self, user_id, name, email, department, designation):
    #     self.user_id = user_id
    #     self.name = name
    #     self.email = email
    #     self.department = department
    #     self.designation = designation

    def json(self):
        return {"user_id": self.userid, "name": self.name, "email": self.email, "department": self.department, "designation": self.designation}

    def get_name(self):
        return self.name

    def get_user_id(self):
        return self.userid

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
        record = Classes.query.filter_by(course_id=course_id,class_id=class_id).first()
        return record
    
    def get_classes_by_course(self, course_id):
        record = Classes.query.filter_by(course_id=course_id).all()
        return record

    #By Xing Jie 
    def get_class_startdate(self, class_id):
        class_A = Classes.query.filter_by(class_id = class_id).first()
        return str(class_A.startdate)

    def get_all_class_sections(self,class_id):
        section_ctrl = Section()
        sections  = section_ctrl.get_section_all(class_id)
        return sections

    def json(self):
        return {"class_id":self.class_id,"course_id":self.course_id,"slots":self.slots,"startdate":self.startdate, "enddate":self.enddate, "trainer_name": self.trainer_name}
    
class Course_Enrollment(db.Model):
    
    __tablename__ = 'COURSE_ENROLLMENT'

    enrollment_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, nullable = False)    
    userid = db.Column(db.Integer, nullable = False)
    class_id = db.Column(db.Integer, nullable = False)
    is_enrolled = db.Column(db.Boolean, nullable = False)

    def add_enrollment_record(self):
        try:
            db.session.add(self)
            db.session.commit()
            db.session.close()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while assigning the class to learner " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "Learner has succesSfully enrolled into a class by HR"
            }
        ), 200
    
    def delete_enrollment_record(self, user_id, class_id, course_id):
        enrollment_record = self.query.filter_by(userid = user_id, class_id = class_id, course_id = course_id, is_enrolled = 1).first()
        try:
            db.session.delete(enrollment_record)
            db.session.commit()
            db.session.close()
        except Exception as error:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occured while deleting the enrollment record. " + str(error)
                }
            )

        return jsonify(
            {
                "code": 200,
                "message": "The enrollment record has been successfully deleted"
            }
        ), 200

    def get_user_enrolled_courses(self, user_id):
        record = Course_Enrollment.query.filter_by(userid=user_id).all()
        return record
    
    def json(self):
        return {"enrollment_id":self.enrollment_id,"course_id":self.course_id,"userid":self.userid, "class_id":self.class_id, "is_enrolled":self.is_enrolled }

    def get_all_enrollments(self):
        all_enrollments = Course_Enrollment.query.all()
        if len(all_enrollments):

            for records in all_enrollments:
                if records.is_enrolled == False:
                    records.is_enrolled = "Pending"

            return jsonify(
                {
                    "code":200,
                    "data": {
                        "enrollment_records" : [records.json() for records in all_enrollments]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There is no enrollment records!"
            }
        ),404


    def set_enrollment_status(self,enrollment_id):
        courseEnrollRecord = Course_Enrollment.query.filter_by(enrollment_id = enrollment_id).first()
        if courseEnrollRecord.is_enrolled == False:
            courseEnrollRecord.is_enrolled = True
            try:
                db.session.commit()
                db.session.close()
            except Exception as error:
                return jsonify({
                    "code": 500,
                    "message": "An error occured while changing the enrollment status " + str(error)
                })

            return jsonify({
                    "code": 500,
                    "message": "Changed enrollment status to True!"
                })

        else:
            courseEnrollRecord.is_enrolled = False
            try:
                db.session.commit()
                db.session.close()
            except Exception as error:
                return jsonify({
                    "code": 500,
                    "message": "An error occured while changing the enrollment status " + str(error)
                })

            return jsonify({
                    "code": 500,
                    "message": "Changed enrollment status to False!"
                })
    
    def rejectEnrollment(self, enrollment_id):
        Course_Enrollment.query.filter_by(enrollment_id = enrollment_id).delete()
        try:
            db.session.commit()
            db.session.close()
        except Exception as error:
            return jsonify({
                "code": 500,
                "message": "There was an error when rejecting enrollment record " + str(error)
            })

        return jsonify({
                "code": 200,
                "message": "Enrollment status of this learner has been rejected"
            })

    def get_course_and_class_id(self):
        return self.course_id,self.class_id

class Course_Prerequisites(db.Model):
    __tablename__ = 'COURSE_PREREQUISITE'

    course_id = db.Column(db.Integer, primary_key=True)
    prereq_course_id = db.Column(db.Integer, primary_key=True)

    def add_prerequisites(self):
        try:
            db.session.add(self)
            db.session.commit()
            db.session.close()
        except Exception as error:
            return jsonify(
                {
                    "code": 500,
                    "message": "There was an error when adding the prerequisite. " + str(error)
                }
            ), 500
        
        return jsonify(
            {
                "code": 200,
                "message": "The prerequisite has been successfully added"
            }
        ), 200

    def prereq_by_course(self,course_id):
        record = Course_Prerequisites.query.filter_by(course_id=course_id).all()
        return record
    
    def json(self):
        return {"course_id": self.course_id, "prereq_course_id": self.prereq_course_id}

class Course(db.Model):
    __tablename__ = 'COURSE'

    # this is equivalent to the __init__ statement for classes but a flask implementation of it
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.String(300), nullable=False)
    startenrollmentdate = db.Column(db.DateTime, nullable=False)
    endenrollmentdate = db.Column(db.DateTime, nullable=False)

    def get_all_courses(self):
        return Course.query.all()

    def get_course_by_id(self, course_id):
        record = Course.query.filter_by(course_id=course_id).first()
        return record

    def add_course(self):
        # this should check if there is already an existing course in the database. To be added later
        try: 
            db.session.add(self)
            db.session.commit()
            db.session.close()
            
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while creating the course. " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The course has been successfully created"
            }
        ), 200
    
    def get_course_name(self):
        return self.course_name

    def del_course(self, course_id):
        course = self.query.filter_by(course_id=course_id).first()
        try: 
            db.session.delete(course)
            db.session.commit()
            db.session.close()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while deleting the course. " + str(error)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "message": "The course has been successfully deleted"
            }
        ), 200
    
    def get_vacancies_by_courses(self, course_id):
        vacant_classes = Classes()
        class_by_course = vacant_classes.get_classes_by_course(course_id)
        course_vacancies = 0

        for a_class in class_by_course:
            course_vacancies += a_class.slots
        
        return course_vacancies

    def change_start_end_date(self, course_id, start_date, end_date):
        record = Course.query.filter_by(course_id = course_id).first()
        record.startenrollmentdate = start_date
        record.endenrollmentdate = end_date
        try:
            db.session.commit()
            db.session.close()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "A database error occured while changing the start and end date of the course " + str(error)
                }
            ), 500

        return jsonify (
                {
                    "code": 200,
                    "message": "The start and end date of the course has been successfully changed"
                }
            ), 200
        
   
    def json(self):
        return {"course_id": self.course_id, "course_name": self.course_name, "course_description": self.course_description, "startenrollmentdate": self.startenrollmentdate, "endenrollmentdate": self.endenrollmentdate}   

class FinalQuiz(db.Model):
    __tablename__ = 'FINAL_QUIZ'
    quiz_id = db.Column(db.Integer, primary_key=True)
    passing_score = db.Column(db.Integer)

    
    def json(self):
        return {"quiz_id": self.quiz_id,"passing_score": self.passing_score}
        
    def get_quiz_id(self):
        return self.quiz_id

    def get_passing_score(self):
        return self.passing_score

    def get_quiz_section(self,quiz_id):
        section = FinalQuiz.query.filter_by(quiz_id = quiz_id).first()
        return section

    def is_graded(self, quiz_id): #Check if quiz_id is in table (If so then quiz is graded)
        exists = db.session.query(FinalQuiz.quiz_id).filter_by(quiz_id= quiz_id).first() is not None 
        if exists:
            pass_score = db.session.query(FinalQuiz.passing_score).filter_by(quiz_id= quiz_id).first()
            db.session.close()
            return pass_score
        else:
            db.session.close()
            return exists

class Learner_Assignment(db.Model):
    __tablename__ = 'LEARNERASSIGNMENT'

    course_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, primary_key=True, index=True)
    userid = db.Column(db.Integer, primary_key=True, index=True)

    def get_user_assigned_courses(self, user_id): 
        record = Learner_Assignment.query.filter_by(userid=user_id).all()
        return record

    def get_course_id(self):
        return self.course_id,self.class_id
    
    def json(self):
        return {"course_id":self.course_id,"class_id":self.class_id, "userid":self.userid}

    def assign_class(self):

        try:
            db.session.add(self)
            db.session.commit()
            db.session.close()
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
                "message": "The class has been successfully assigned to the Learner"
            }
        ), 200

    def delete_learner_assignment(self,course_id,class_id,user_id):
        lrnr_as_record = self.query.filter_by(course_id = course_id, class_id=class_id,userid = user_id).first()
        try:
            db.session.delete(lrnr_as_record)
            db.session.commit()
            db.session.close()
        except Exception as error:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occured while deleting the learner assignment record. " + str(error)
                }
            )

        return jsonify(
            {
                "code": 200,
                "message": "The learner assignment record has been successfully deleted"
            }
        ), 200

class Learner_Badges(db.Model):
    __tablename__ = 'LEARNER_BADGES'

    userid = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, primary_key=True)

    def json(self):
        return {"user_id": self.userid, "course_id": self.course_id}

    def get_learner_badges(self, user_id):
        record = self.query.filter_by(userid=user_id).all()
        return record

class Learner(User):
    __tablename__ = 'learners'

    __mapper_args__ = {'polymorphic_identity': 'learner'}

    def get_all_learners(self):
        records = Learner.query.filter_by(designation='Junior Engineer').all()
        records2 = Learner.query.filter_by(designation='Senior Engineer').all()
        records3 = records + records2
        return records3

    def get_all_learners_id(self):
        records = Learner.query.with_entities(Learner.userid).all()
        return records
    
    # def is_learner(self, user_id):
    #     lrnr = Learner.query.filter_by(userid=user_id).first()
    #     return lrnr
    
    def get_course_class (self, course_list):
        course_class = Course()
        classes_class = Classes()
        courses = [course_class.get_course_by_id(a_course.course_id) for a_course in course_list]
        classes = []
        for a_course in course_list:
            classinfo = classes_class.get_classes_by_course(a_course.course_id)
            for a_class in classinfo:
                classes.append(a_class)
        return [courses, classes]
    
    def get_enrolled_courses(self, user_id):
        enrolled_courses = Course_Enrollment()
        enrolled_courses_list = enrolled_courses.get_user_enrolled_courses(user_id)        
        output = [enrolled_course for enrolled_course in enrolled_courses_list if enrolled_course.is_enrolled == 1]
        return output
    
    def get_enrolled_course_class(self, user_id): 
        enrolled_courses = self.get_enrolled_courses(user_id)  
        enrolled_courses_list = [enrolled_course for enrolled_course in enrolled_courses]
        output = self.get_course_class(enrolled_courses_list)
        return output

    def get_assigned_courses(self, user_id): 
        assigned_courses = Learner_Assignment()
        assigned_courses_list = assigned_courses.get_user_assigned_courses(user_id)
        output = [assigned_course for assigned_course in assigned_courses_list]
        return output
    
    def get_assigned_course_class(self, user_id): 
        assigned_courses = Learner_Assignment()
        assigned_courses_list = assigned_courses.get_user_assigned_courses(user_id)
        output = self.get_course_class(assigned_courses_list)
        return output

    def get_completed_courses(self, user_id):
        completed_courses = Learner_Badges()
        course_class = Course()
        completed_courses_list = completed_courses.get_learner_badges(user_id)
        output = [course_class.get_course_by_id(completed_course.course_id) for completed_course in completed_courses_list]
        return output

    def get_remaining_courses(self, user_id):
        learner_badges = Learner_Badges()
        course_class = Course()
        course_list = [course.course_id for course in course_class.get_all_courses()]
        completed_courses = [course.course_id for course in learner_badges.get_learner_badges(user_id)]
        enrolled_courses = [course for course in self.get_enrolled_courses(user_id)]
        assigned_courses = [course for course in self.get_assigned_courses(user_id)]
        completed_enrolled_assigned_courses = completed_courses + enrolled_courses + assigned_courses
        remaining_course = [course for course in course_list if course not in completed_enrolled_assigned_courses]
        output = [course_class.get_course_by_id(course_query) for course_query in remaining_course if course_class.get_vacancies_by_courses(course_query) > 0]
        return output

    def get_eligible_courses(self, userid):
        course_class = Course()
        classes_class = Classes()
        course_pre_req = Course_Prerequisites()
        learner_badges = Learner_Badges()
        completed_courses = learner_badges.get_learner_badges(userid)

        course_list = [course.course_id for course in self.get_remaining_courses(userid)]
        
        # output = []
        course_query_list = []

        for course_query in course_list: 
            prereqlist = course_pre_req.prereq_by_course(course_query)
            if len(prereqlist) == 0: 
                course_query_list.append(course_query)
            else: 
                for course in prereqlist: 
                    if course.prereq_course_id in completed_courses:
                        course_query_list.append(course_query)
        
        courses = []
        classes = []
        for course in course_query_list:
            course_classes = classes_class.get_classes_by_course(course)
            for a_class in course_classes:
                if a_class.slots > 0: 
                    course_info = course_class.get_course_by_id(course)
                    courses.append(course_info)
                    classes.append(a_class)

        return [courses, classes]

    def get_eligible_classes(self, user_id):
        course_class = Course()
        classes_class = Classes()
        output = self.get_eligible_courses(user_id)
        course_query_list = output[0]
        courses = []
        classes = []
        for course in course_query_list:
            print("course: " + str(course))
            course_classes = classes_class.get_classes_by_course(course.course_id)
            for a_class in course_classes:
                if a_class.slots > 0: 
                    course_info = course_class.get_course_by_id(course.course_id)
                    courses.append(course_info)
                    classes.append(a_class)
        
        return [courses, classes]

    def get_uneligible_courses(self, user_id):
        course_class = Course()
        course_list = [course.course_id for course in self.get_remaining_courses(user_id)]
        eligible_courses = [course for course in self.get_eligible_courses(user_id)]
        other_courses = [course for course in course_list if course not in eligible_courses]
        output = [course_class.get_course_by_id(course_query) for course_query in other_courses]
        return output

class multiplechoiceoptions(db.Model):
    __tablename__ = 'MCQ_OPTIONS'
    question_id= db.Column(db.Integer, primary_key=True)
    option_order = db.Column(db.Integer, primary_key=True)
    option_content = db.Column(db.String(500))
    correct_option = db.Column(db.Boolean)
    
    
    def json(self):
       return {"question_id": self.question_id,"option_order": self.option_order,"option_content": self.option_content,"correct_option": self.correct_option}
        
    def get_question_id(self):
        return self.question_id

    def get_option_order(self):
        return self.option_order

    def get_option_content(self):
        return self.option_content

    def get_correct_option(self):
        return self.correct_option
        
    def get_options_by_question_id(self,question_id):
        option= self.query.filter_by(question_id = question_id)
        db.session.close()
        return option
    
    def create_MCQ_options(self):
        try: 
            db.session.add(self)
            db.session.commit()
            # db.session.close()
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
                "data":self.json()
            }
        ), 200

class QuizQuestions(db.Model):
    __tablename__ = 'QUIZ_QUESTION'
    question_id= db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer)
    qorder = db.Column(db.Integer)
    question_type = db.Column(db.String(100))
    question = db.Column(db.String(500))
    __mapper_args__ ={
        'polymorphic_identity': question_type
    }

    def json(self):
        return {"question_id": self.question_id,"quiz_id": self.quiz_id, "qorder": self.qorder,"question_type": self.question_type,"question": self.question }

    def get_quiz_id(self):
        return self.quiz_id

    def get_question_id(self):
        return self.question_id

    def get_question_type(self):
        return self.question_type
    
    def get_qorder(self):
        return self.qorder

    def get_question(self):
        return self.question

    def get_all_questions(self,quiz_id):
        questions = self.query.filter_by(quiz_id = quiz_id)
        return questions

    def create_MCQ(self):
        try: 
            db.session.add(self)
            db.session.commit()
            # db.session.close()
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
                "id": self.get_question_id()
            }
        ), 200
    
    def get_mcq_question_options(self,question_id):
        mcq_ctrl = multiplechoiceoptions()
        option = mcq_ctrl.get_options_by_question_id(question_id)
        if option:
            return jsonify(
                {
                    
                    "data": [question.json() for question in option]
                })
        return jsonify(
            {
                "code": 404,
                "message": "There are no section."
            }
        )
      
class Quiz(db.Model):
    __tablename__ = 'QUIZZES'
    quiz_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer)
    time_limit = db.Column(db.Integer)
    question = []
    

    def json(self):
        return {"quiz_id": self.quiz_id,"section_id": self.section_id, "time_limit": self.time_limit}

    def get_quiz_id(self):
        return self.quiz_id

    def get_section_id(self):
        return self.section_id

    def get_time_limit_with_id(self, quiz_id):
        quizObj = Quiz.query.filter_by(quiz_id= quiz_id).first()
        timer = quizObj.time_limit
        db.session.close()
        return str(timer)

    def get_section_id_with_quiz_id(self, quiz_id):
        quizObj = Quiz.query.filter_by(quiz_id= quiz_id).first()
        section_id = quizObj.section_id
        db.session.close()
        return section_id

    def get_quizzes(self,section_id):
        quizzes = self.query.filter_by(section_id=section_id)
        db.session.close()
        return quizzes
        
    def add_questions(self,questions):
        self.question.append(questions)

    def get_quiz_by_id(self,quiz_id):
        try:
            quizzes = Quiz.query.filter_by(quiz_id=quiz_id).first()
            db.session.close()
        except Exception as error:
            return jsonify(
                {
                    "code": 404,
                    "message": "There are no quiz."
                }
            )
        
        return jsonify(
            {
                "code": 200,
                "data": quizzes.json()
            })
    
    def create_quiz(self):
        try: 
            db.session.add(self)
            db.session.commit()
            # db.session.close()
        except Exception as error:
            return jsonify (
                {
                    "code": 500,
                    "message": "An error occured while creating the section. " + str(error)
                }
            ), 500

        # print("quiz_entry.get_quiz_id(): " + str(quiz_entry.get_quiz_id()))

        return jsonify(
            {
                "code": 200,
                "message": "The section has been successfully created",
                "quiz_id": self.get_quiz_id()
            }
        ), 200

    def delete_Quiz(self,quiz_id):
        record_obj = self.query.filter(quiz_id== quiz_id)
        try:
            db.session.delete(record_obj)
            db.session.commit()
            db.session.close()
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
                "message": "The quiz has been successfully deleted"
            }
        ), 200

    def get_quiz_questions(self,quiz_id):
        quiz_qn_ctrl = QuizQuestions()
        questions = quiz_qn_ctrl.get_all_questions(quiz_id)
        
        if questions:
            return jsonify(
                {
                    "code": 200,
                    "data": [question.json() for question in questions]
                })
        return jsonify(
            {
                "code": 404,
                "message": "There are no section."
            }
        )

    def get_final_quiz(self,quiz_id):
        final_quiz_ctrl = FinalQuiz()
        section = final_quiz_ctrl.get_quiz_section(quiz_id)
        return section
        
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

    def get_section_title_with_id(self, section_id):
        section = Section.query.filter_by(section_id= section_id).first()
        section_title = section.section_title
        db.session.close()
        return section_title

    def get_sections(self, section_id):
        section = Section.query.filter_by(section_id=section_id).first()
        db.session.close()
        return section

    def get_section_all(self,class_id):
        sections  = self.query.filter_by(class_id=class_id)
        db.session.close()
        
        if sections:
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
    
    def create_section(self):
        try: 
            db.session.add(self)
            db.session.commit()
            db.session.close()
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

    def get_all_section_materials(self, section_id):
        section_materials_ctrl = SectionMaterials()
        materials = section_materials_ctrl.get_materials_all(section_id)
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

    def get_latest_quiz(self,section_id):
        quiz_ctrl = Quiz()
        quizzes = quiz_ctrl.get_quizzes(section_id)
        last_id = quizzes[-1]
        return jsonify(
            {
                "code": 200,
                "data": last_id.json()
            })

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
        materials = self.query.filter_by(section_id=section_id).all
        return materials

    def create_material(self):
        try: 
            db.session.add(self)
            db.session.commit()
            db.session.close()
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
            db.session.close()
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

class Trainer(User):
    __tablename__ = 'TRAINERS'

    __mapper_args__ = {'polymorphic_identity': 'trainer'}
    userid = db.Column(db.Integer, db.ForeignKey('USERS.userid'), primary_key=True)
    
    # def is_trainer(self, userid):
    #     trnr = Trainer.query.filter_by(userid=userid).first()
    #     return trnr

    def get_user_id(self):
        return self.userid
    
    def get_all_trainers(self):
        trnr = Trainer()
        return trnr.query.filter_by(designation='Senior Engineer').all()

    def get_assigned_classes(self,user_id):
        
        classes = Trainer_Assignment.query.filter_by(userid=user_id)

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

class TrueFalse(QuizQuestions):
    __tablename__ = 'TRUEFALSEQ'
    
    question_id = db.Column(db.Integer, db.ForeignKey('QUIZ_QUESTION.question_id'), primary_key=True)
    answer = db.Column(db.Boolean)
    __mapper_args__ = {'polymorphic_identity': 'TF','inherit_condition': (question_id == QuizQuestions.question_id)}
    
    def json(self):
        return {"answer":self.answer,"question_id": self.question_id,"quiz_id": self.quiz_id, "qorder": self.qorder,"question_type": self.question_type,"question": self.question }
        
    def get_question_id(self):
        return self.question_id


    def get_answer(self):
        return self.answer

    def get_true_false_options(self,question_id):
        tf = TrueFalse.query.filter_by(question_id=question_id).first()
        db.session.close()
        return tf

    def get_quiz_questions(self,question_id):
        questions = TrueFalse.query.filter_by(question_id =question_id)
        #check if empty
        y = self.get_qorder()
        count =0
        db.session.close()
        for x in questions:
            count+=1

        if count!=0:
            return jsonify(
                {
                    
                    "data": [question.json() for question in questions]
                })
        return jsonify(
            {
                "code": 404,
                "message": "There are no section."
            }
        )

    def create_TrueFalse(self):        
        try: 
            db.session.add(self)
            db.session.commit()
            db.session.close()
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

class multiplechoice(QuizQuestions):
    __tablename__ = 'MCQ'
    question_id= db.Column(db.Integer,db.ForeignKey('QUIZ_QUESTION.question_id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'MCQ','inherit_condition': (question_id == QuizQuestions.question_id)}

    def json(self):
        return {"question_id": self.question_id,"quiz_id": self.quiz_id, "qorder": self.qorder,"question_type": self.question_type,"question": self.question }

class Ungraded_quiz_score(db.Model):
    __tablename__ = 'UNGRADED_QUIZ_SCORE'

    userid = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_score = db.Column(db.Float, nullable=True)
    time_inserted = db.Column(db.DateTime, primary_key=True)

    def json(self):
        return {"user_id": self.userid, "quiz_id": self.quiz_id, "quiz_score": self.quiz_score, "time_inserted" : datetime.now()}

    def insert_score(self, scoreObj): 
        
        scoreRecord = Ungraded_quiz_score(userid = scoreObj['user_id'], quiz_id = scoreObj['quiz_id'], quiz_score = scoreObj['quiz_score'], time_inserted = datetime.now())
        db.session.add(scoreRecord)
        db.session.commit()
        db.session.close()
        return "Success"

class Graded_quiz_score(db.Model):
    __tablename__ = 'GRADED_QUIZ_SCORE'

    userid = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_score = db.Column(db.Float, nullable=True)
    result = db.Column(db.Boolean, nullable = True)
    time_inserted = db.Column(db.DateTime, primary_key = True)


    def json(self):
        return {"user_id": self.userid, "quiz_id": self.quiz_id, "quiz_score": self.quiz_score, "result": self.result, "time_inserted" : datetime.now()}

    def insert_score(self, scoreObj): 
        
        scoreRecord = Graded_quiz_score(userid = scoreObj['user_id'], quiz_id = scoreObj['quiz_id'], quiz_score = scoreObj['quiz_score'], result = scoreObj['result'], time_inserted = datetime.now())
        db.session.add(scoreRecord)
        db.session.commit()
        db.session.close()
        return "Success"

# list of controllers
# 1. assign_controller (REMOVED)
# 2. course_controller (REMOVED)
# 3. enrollment_controller 
# 4. sectionmaterialcontroller 
# 5. sectionquizcontroller
# 6. view_controller 

'''
Functionalities of assign_controller
'''
# class AssignController(): # all functionalities of this controller have been moved into the routes
    # def assign_trainer(self,course_id,class_id,hr_id,trainer_id):

    #     usr = User()
    #     trnr = Trainer()

    #     valid_hr = usr.is_hr(hr_id)

    #     valid_trnr = trnr.is_trainer(trainer_id)

    #     course_to_assign = request.get_json()
    #     print("Request to assign course to user is received")

    #     if valid_hr and valid_trnr:
    #         #return assignment of course

    #         print("HR is assigning a class of a course to a trainer")

    #         userid = course_to_assign['trainer_id']
    #         course_id = course_to_assign['course_id']
    #         class_id = course_to_assign['class_id']

    #         trainer_assignement_entry = Trainer_Assignment(course_id = course_id, class_id = class_id,userid = userid)

    #         return trainer_assignement_entry.assign_class()
        
    #     else:
    #         #reject user from assigning courses
    #         return jsonify(
    #             {
    #                 "code": 404,
    #                 "message": "You either have no permission as a HR or the assigned user is not a trainer"
    #             }
    #         ), 404

    # def get_assignment_trainer(self,userid):

    #     trnr = Trainer()
        
    #     if trnr:

    #         print("Retrieving Trainer ", userid , "'s assigned classes")
    #         return trnr.get_assigned_classes(userid)
            
    #     else:
    #         #reject user from retrieving
    #         return jsonify(
    #             {
    #                 "code": 404,
    #                 "message": "user id does not belong to a valid Trainer"
    #             }
    #         ), 404

    # def assign_learner(self,course_id,class_id,hr_id,learner_id):

    #     usr = User()

    #     lrnr = Learner()

    #     valid_hr = usr.is_hr(hr_id)
    #     valid_lrnr = lrnr.is_learner(learner_id)

    #     class_to_assign = request.get_json()

    #     if valid_hr and valid_lrnr:

    #         print("HR is assigning and enrolling learner to a class of a course")


    #         userid = class_to_assign['learner_id']
    #         course_id = class_to_assign['course_id']
    #         class_id = class_to_assign['class_id']

    #         course_enrollment_entry = Learner_Assignment(course_id = course_id, userid = userid, class_id = class_id)

    #         return course_enrollment_entry.assign_class()

'''
Functionalities of class_controller.... THERE ARE NONE
'''


'''
Functionalities of course_controller
'''
# class CourseController(): # all functionalities of this controller have been moved into the routes
    # def create_course(self, user_id, application):
    #     # employee_da = EmployeeDataAccess()
    #     print("Request to create a course received")

    #     # call validate_hr in employee data access class
    #     # valid_hr = employee_da.validate_hr(user_id)

    #     # if valid_hr: # boolean return
    #     print("HR is requesting to create a new course")
    #     course_name = application["course_name"]
    #     course_description = application["course_description"]
    #     start_enrollment_date = application["start_enrollment_date"]
    #     end_enrollment_date = application["end_enrollment_date"]

    #     # check that all fields are not empty
    #     if all(field is not None for field in [course_name, course_description, start_enrollment_date, end_enrollment_date]):
    #         course_entry = Course(course_name=course_name, course_description=course_description, startenrollmentdate=start_enrollment_date, endenrollmentdate=end_enrollment_date)
            
    #         status = course_entry.add_course()
    #         # print(status["code"])
    #         return status

    # def delete_course(self, user_id, application):
    #     print("HR is requesting to delete an existing course")
    #     course_id = application["course_id"]
    #     course_entry = Course()
    #     return course_entry.del_course(course_id)

    #Xing Jie parts
    # def retrieveAllEnrollment(self):
    #     enrollmentDA = CourseEnrollmentDataAccess()
    #     enrollments = enrollmentDA.retrieveAllEnrollments()
    #     return enrollments

    # def changeEnrollmentStatus(self, enrollment_id):
    #     enrollmentDA = Course_Enrollment()
    #     output = enrollmentDA.set_enrollment_status(enrollment_id)
    #     return output

    # def retrieveEnrollmentsBeforeStart(self):
    #     enrollmentDA = Course_Enrollment()
    #     output = enrollmentDA.retrieveEnrollmentsBeforeStart()
    #     return output
     
    # def rejectEnrollment(self, enrollment_id):
    #     enrollmentDA = Course_Enrollment()
    #     output = enrollmentDA.rejectEnrollment(enrollment_id)
    #     return output


'''
Functionalities of enrollment_controller
'''
class EnrollmentController():
    def apply_class(self, application):
        userid = application['user_id']
        class_id = application['class_id']
        course_id = application['course_id']
        is_enrolled = 0

        # check if fulfilled prerequisites
        completed_courses = Learner_Badges()
        course_prereq = Course_Prerequisites()
        fulfilled_prereq = completed_courses.get_learner_badges(userid)
        prerequisites = course_prereq.prereq_by_course(course_id)
        completed = [course.course_id for course in fulfilled_prereq]
        prereq = [course.prereq_course_id for course in prerequisites]

        print("completed: " + str(completed))
        print("prereq" + str(prereq))

        if not all(item in completed for item in prereq):
            not_completed = [course for course in prereq if course not in completed]
            return jsonify(
                {
                    "message": "The following courses have not been completed",
                    "incomplete_courses": not_completed
                }
            )
        
        # check if there is capacity
        classes = Classes()
        capacity = classes.getSlots(class_id)
        if capacity == 0:
            return jsonify(
                {
                    "message": "The class that you are trying to enroll has no more spots"
                }
            )

        course_enrollment_ctrl = Course_Enrollment(course_id = course_id, userid = userid, class_id = class_id, is_enrolled = is_enrolled)
        return course_enrollment_ctrl.add_enrollment_record()
    
    # def drop_class(self, application):
    #     user_id = application['user_id']
    #     class_id = application['class_id']
    #     course_id = application['course_id']

    #     course_enrollment_ctrl = Course_Enrollment()
    #     return course_enrollment_ctrl.delete_enrollment_record(user_id, class_id, course_id)


'''
Functionalities of section_material_quiz_controller
'''
# class SectionMaterialQuizController(): # all functionalities of this controller have been moved into the routes
    # def view_qn(self,quiz_id):
    #     da = TrueFalse()
    #     questions = da.get_quiz_questions(quiz_id)
    #     return questions
        

    # def get_material_record_by_section(self, section_id):
    #     if section_id >0:
    #         da = SectionMaterials()
    #         materials = da.get_materials_all(section_id)
    #         return materials
    #     else:
    #         raise Exception ("Section Id must be above 0");
    
    # def get_sections_by_class(self,class_id):
    #     da = Section()
    #     section = da.get_section_all(class_id)
    #     return section

    # def get_section_quiz(self,section_id):
    #     da = Quiz()
    #     section = da.get_quiz(section_id)
    #     return section

    # def get_quiz_questions(self,quiz_id):
    #     da = QuizQuestions()
    #     questions = da.get_quiz_questions(quiz_id)
    #     return questions

    

    # def create_section(self,class_id,section_title):
        
    #     section_entry = Section(class_id = class_id,section_title=section_title)
    #     try: 
    #         db.session.add(section_entry)
    #         db.session.commit()
    #         db.session.close()
    #     except Exception as error:
    #         return jsonify (
    #             {
    #                 "code": 500,
    #                 "message": "An error occured while creating the section. " + str(error)
    #             }
    #         ), 500

    #     return jsonify(
    #         {
    #             "code": 200,
    #             "message": "The section has been successfully created"
    #         }
    #     ), 200
    
    # def create_quiz(self,section_id,time_limit):
    #     quiz_entry = Quiz(section_id = section_id,time_limit=time_limit)
    #     try: 
    #         db.session.add(quiz_entry)
    #         db.session.commit()
    #         # db.session.close()
    #     except Exception as error:
    #         return jsonify (
    #             {
    #                 "code": 500,
    #                 "message": "An error occured while creating the section. " + str(error)
    #             }
    #         ), 500

    #     print("quiz_entry.get_quiz_id(): " + str(quiz_entry.get_quiz_id()))

    #     return jsonify(
    #         {
    #             "code": 200,
    #             "message": "The section has been successfully created",
    #             "quiz_id": quiz_entry.get_quiz_id()
    #         }
    #     ), 200

    # def create_material(self,section_id,material_title,material_content,material_type):
    #     material_entry = SectionMaterials(section_id=section_id,material_title=material_title,material_content=material_content,material_type=material_type)

    #     try: 
    #         db.session.add(material_entry)
    #         db.session.commit()
    #         db.session.close()
    #     except Exception as error:
    #         return jsonify (
    #             {
    #                 "code": 500,
    #                 "message": "An error occured while creating the material. " + str(error)
    #             }
    #         ), 500

    #     return jsonify(
    #         {
    #             "code": 200,
    #             "message": "The material has been successfully created"
    #         }
    #     ), 200

    # def create_TrueFalse(self,answer,quiz_id,qorder,question_type,question):
    #     question_entry = TrueFalse(quiz_id = quiz_id, answer = answer, qorder = qorder, question_type = question_type, question=question)
        
    #     try: 
    #         db.session.add(question_entry)
    #         db.session.commit()
    #         db.session.close()
    #     except Exception as error:
    #         return jsonify (
    #             {
    #                 "code": 500,
    #                 "message": "An error occured while creating the question. " + str(error)
    #             }
    #         ), 500

    #     return jsonify(
    #         {
    #             "code": 200,
    #             "message": "The question has been successfully created"
    #         }
    #     ), 200

    # def create_MCQ(self,quiz_id,qorder,question_type,question):
    #     question_entry = QuizQuestions(quiz_id=quiz_id,question_type=question_type,qorder=qorder,question=question)
    #     try: 
    #         db.session.add(question_entry)
    #         db.session.commit()
    #         # db.session.close()
    #     except Exception as error:
    #         return jsonify (
    #             {
    #                 "code": 500,
    #                 "message": "An error occured while creating the question. " + str(error)
    #             }
    #         ), 500

    #     return jsonify(
    #         {
    #             "code": 200,
    #             "message": "The question has been successfully created",
    #             "id": question_entry.get_question_id()
    #         }
    #     ), 200

    # def create_MCQ_options(self,question_id,option_order,option_content,correct_option):
        
    #     option_entry = multiplechoiceoptions(question_id = question_id,option_order =option_order,option_content = option_content,correct_option = correct_option)
    #     print('entry c-option is ',option_entry.get_correct_option())
    #     try: 
    #         db.session.add(option_entry)
    #         db.session.commit()
    #         # db.session.close()
    #     except Exception as error:
    #         return jsonify (
    #             {
    #                 "code": 500,
    #                 "message": "An error occured while creating the option. " + str(error)
    #             }
    #         ), 500

    #     return jsonify(
    #         {
    #             "code": 200,
    #             "message": "The option has been successfully created",
    #             "data":option_entry.json()
    #         }
    #     ), 200

    # def get_TrueFalse(self,question_id):
    #     da = TrueFalse()
    #     questions = da.get_quiz_questions(question_id)
    #     return questions
    
    # def get_MCQ(self,question_id):
    #     da = multiplechoiceoptions()
    #     questions = da.get_options_by_question_id(question_id)
    #     return questions

    # def delete_Quiz(self,quiz_id):
    #     '''delete_quiz =QuizQuestions.query.filter_by(quiz_id = quiz_id).delete()
    #     delete_tf = TrueFalse.query.filter_by(quiz_id = quiz_id).delete()'''
    #     record_obj = db.session.query(TrueFalse).filter(TrueFalse.quiz_id== quiz_id)
    #     db.session.delete(record_obj)
    #     db.session.commit()
    #     db.session.close()
        # '''
        # try: 
        #     db.session.delete(delete_tf)
        #     db.session.delete(delete_quiz)
        #     db.session.commit()
        # except Exception as error:
        #     return jsonify (
        #         {
        #             "code": 500,
        #             "message": "An error occured while deleting the quiz. " + str(error)
        #         }
        #     ), 500

        # return jsonify(
        #     {
        #         "code": 200,
        #         "message": "The questions has been successfully quiz",
                
        #     }
        # ), 200'''


'''
Functionalities of view_controller
'''
class ViewController():
    def get_courses_with_classes_without_trainer():
        trnr_as_class = Trainer_Assignment()
        course_class = Course()
        classes_class = Classes()

        course_list = [course.course_id for course in course_class.get_all_courses()]
        courses_with_trainers = [(course.course_id, course.class_id) for course in trnr_as_class.get_all_trainer_assignments()]

        crse_with_class_without_trainers = []
        output = []

        for crse in course_list:
            classesOfCrseList = [classes.class_id for classes in classes_class.get_classes_by_course(crse)] 
            
            for cl in classesOfCrseList:
                if (crse,cl) not in courses_with_trainers:
                    if(crse not in output):
                        crse_with_class_without_trainers.append(crse)
        
        for crse in crse_with_class_without_trainers:
            output.append(course_class.get_course_by_id(crse))

        print(output)
        
        return output

    def get_classes_of_a_course_without_trainer(course_id):
        trnr_as_class = Trainer_Assignment()
        classes_class = Classes()

        courses_with_trainers = [(course.course_id, course.class_id) for course in trnr_as_class.get_all_trainer_assignments()]
        classesOfCrseList = [classes.class_id for classes in classes_class.get_classes_by_course(course_id)] 
        output = []
        classes_without_trainer = []
        for cl in classesOfCrseList:
            if (course_id,cl) not in courses_with_trainers:
                if(cl not in output):
                    classes_without_trainer.append(cl)
                        
        print(classes_without_trainer)
        for cl in classes_without_trainer:
            output.append(classes_class.get_classes_by_class_id(course_id,cl))

        print(output)

        return output

    # def get_learner_assigned_classes(user_id):
    #     lrnr_class = Learner_Assignment()
    #     all_assigned_courses = lrnr_class.get_user_assigned_courses(user_id)

    #     return all_assigned_courses

    # def get_learner_enrolled_classes(user_id):
    #     crse_enrol_class = Course_Enrollment()
        
    #     return crse_enrol_class.get_user_enrolled_courses(user_id)


'''


SACRED MOSES SPLIT



'''


'''
Routes of assign_controller
'''
@app.route("/assign_course_trainer", methods=['POST'])
def assign_course_trainer():
    application = request.get_json(force=True)
    print("HR is assigning a class of a course to a trainer")

    userid = application['trainer_id']
    course_id = application['course_id']
    class_id = application['class_id']

    trainer_assignment_entry = Trainer_Assignment(course_id = course_id, class_id = class_id,userid = userid)

    return trainer_assignment_entry.assign_class()

@app.route("/get_assigned_courses",methods = ['POST'])
def get_assigned_classes_trainer():
    application = request.get_json(force=True)
    userid = application['userid']
    trnr = Trainer()
    return trnr.get_assigned_classes(userid) # this output is weird as fuck

@app.route("/assign_course_learner", methods= ['POST'])
def assign_course_learner():
    application = request.get_json(force=True)
    course_id = application['course_id']
    class_id = application['class_id']
    userid = application['learner_id']
    
    print("HR is assigning and enrolling learner to a class of a course")
    course_enrollment_entry = Learner_Assignment(course_id = course_id, userid = userid, class_id = class_id)

    return course_enrollment_entry.assign_class()

@app.route('/delete_assigned_classes', methods = ['POST'])
def delete_assigned_classes():
    application = request.get_json(force=True)
    course_id = application['course_id']
    class_id = application['class_id']
    user_id = application['user_id']

    lrnr_as_class = Learner_Assignment()
    return lrnr_as_class.delete_learner_assignment(course_id,class_id,user_id)


'''
Routes of class_controller
'''
@app.route("/get_classes/<course_id>", methods=['POST'])
def get_all_classes(course_id):
    print(course_id)
    class_ctrl = Classes()
    record =  class_ctrl.get_classes_by_course(course_id)
    print(record)
    if len(record):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "record": [a_record.json() for a_record in record]
                }
            }
        )
    
    return jsonify(
    {
        "code": 404,
        "message": "There are no classes."
        }
    ), 404

@app.route("/get_startDate/", methods=['POST'])
def getClassStartDate():
    class_id = request.data
    searchIds = json.loads(class_id.decode('utf-8'))
    class_ctrl = Classes()
    

    print(searchIds['ids'], file=sys.stderr)
    searchIds = searchIds['ids']
    approvedEnrollments = []

    counter = 0
    for x in searchIds:
        startDate = class_ctrl.get_class_startdate(x)
        #print(startDate, file=sys.stderr)
        dateToCompare =datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
        if datetime.now() < dateToCompare:
            approvedEnrollments.append(counter)
        counter += 1
    print(approvedEnrollments, file=sys.stderr)
    return json.dumps(approvedEnrollments)


'''
Routes of course_controller
'''
@app.route("/create_course", methods=['POST'])
def create_course():
    # if request.is_json():
    #     try:
    application = request.get_json()
    user_id = application['user_id']

    print("Request to create a course received")
    course_name = application["course_name"]
    course_description = application["course_description"]
    start_enrollment_date = application["start_enrollment_date"]
    end_enrollment_date = application["end_enrollment_date"]

    if all(field is not None for field in [course_name, course_description]):
        course_entry = Course(course_name=course_name, course_description=course_description, startenrollmentdate=start_enrollment_date, endenrollmentdate=end_enrollment_date)
        
        return course_entry.add_course()

@app.route("/delete_course", methods=['POST'])
def delete_course():
    application = request.get_json()
    print("HR is requesting to delete an existing course")
    course_id = application["course_id"]
    course_entry = Course()
    return course_entry.del_course(course_id)

@app.route("/courses", methods=['GET'])
def get_courses():
    courses = Course()
    record = courses.get_all_courses()
    if len(record):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "record": [a_record.json() for a_record in record]
                }
            }
        )
    return jsonify(
            {
                "code": 404,
                "message": "There are no prerequisites."
            }
        ), 404

@app.route("/prerequisitesbycourse", methods=['GET'])
def prereq_by_course():
    application = request.get_json()
    course_id = application['course_id']
    prereq = Course_Prerequisites()
    record = prereq.prereq_by_course(course_id)
    if len(record):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "record": [a_record.json() for a_record in record]
                }
            }
        )
    return jsonify(
            {
                "code": 404,
                "message": "There are no prerequisites."
            }
        ), 404

@app.route("/changeEnrollmentStatus", methods=["POST"])
def changeEnrollStatus():
    application = request.get_json()
    enrollment_id = application['enrollment_id']
    enrollmentDA = Course_Enrollment()
    return enrollmentDA.set_enrollment_status(enrollment_id)

@app.route("/allEnrollmentsPending", methods=['GET'])
def getAllPendingEnrollment():
    da = Course_Enrollment()
    enrollments = da.get_all_enrollments()
    if enrollments == Null:
        return enrollments
    else:
        astuff = json.loads(enrollments.data.decode('utf-8'))
        enrollment_list = astuff["data"]["enrollment_records"]
        print(enrollment_list, file=sys.stderr)
        #For logging purposes
        class_ids = []
        final_enrollmentList = []
        # for x in enrollment_list: #Replace with sending a list of class_id instead
        #     print(x["class_id"], file=sys.stderr)
        #     class_id = x["class_id"]
        #     r = requests.get('http://localhost:5011/get_startDate/'+ str(class_id))
        #     print(r.text, file=sys.stderr)
        #     dateToCompare =datetime.strptime(r.text, '%Y-%m-%d %H:%M:%S')
        #     if datetime.now() < dateToCompare:
        #         print("Ok", file=sys.stderr)
        #         final_enrollmentList.append(x)
        #     else:
        #         print("No", file=sys.stderr)
        # return final_enrollmentList

        for x in enrollment_list: #Replace with sending a list of class_id instead
            class_ids.append(x["class_id"])
        dataObj = {'ids': class_ids}
        r = requests.post('http://localhost:5000/get_startDate/', data = json.dumps(dataObj))
        dataReceived = r.text
        dataReceived = dataReceived[1:]
        dataReceived = dataReceived[:-1]
        enrolled_list = dataReceived.split(", ")

        
        counter = 0
        for x in enrollment_list:
            #print("Current item: " + str(x), file=sys.stderr)
            if str(counter) in enrolled_list:

                final_enrollmentList.append(x)
            counter += 1
        
        return jsonify(final_enrollmentList)

@app.route("/rejectEnrollment", methods=['POST'])
def rejectEnrollment():
    application = request.get_json()
    enrollment_id = application['enrollment_id']
    enrollmentDA = Course_Enrollment()
    return enrollmentDA.rejectEnrollment(enrollment_id)

@app.route("/change_course_start_end_date", methods=['POST'])
def change_course_start_end_date():
    application = request.get_json()
    course_ctrl = Course()
    course_id = application['course_id']
    start_date = application['start_date']
    end_date = application['end_date']
    status = course_ctrl.change_start_end_date(course_id, start_date, end_date)
    return status


'''
Routes of enrollment_controller
'''
@app.route("/enroll", methods=['POST'])
def apply_class():
    application = request.get_json()
    enroll_ctrl = EnrollmentController()
    return enroll_ctrl.apply_class(application)

@app.route("/drop_class", methods=['POST'])
def drop_class():
    application = request.get_json()
    user_id = application['user_id']
    class_id = application['class_id']
    course_id = application['course_id']

    course_enrollment_ctrl = Course_Enrollment()
    return course_enrollment_ctrl.delete_enrollment_record(user_id, class_id, course_id)


'''
Routes of section_material_controler
'''
@app.route("/view_section_materials", methods=['GET'])
def view_Materials():
    section_id = int(request.args.get('section_id', None))
    if section_id >0:
        da = Section()
        materials = da.get_all_section_materials(section_id)
        return materials
    else:
        raise Exception ("Section Id must be above 0");

@app.route("/view_class_sections", methods=['GET'])
def view_Sections():
    class_id = int(request.args.get('class_id', None))
    da = Classes()
    sections = da.get_all_class_sections(class_id)
    return sections

@app.route("/view_section_quiz", methods=['GET'])
def view_Quiz():
    section_id = int(request.args.get('section_id', None))
    da = Quiz()
    quiz = da.get_latest_quiz(section_id)
    return quiz

@app.route("/create_section", methods=['GET'])
def create_section():
    class_id = int(request.args.get('class_id', None))
    section_title = str(request.args.get('section_title', None))
    da = Section(class_id,section_title)
    status = da.create_section()
    return status

@app.route("/create_quiz", methods=['GET'])
def create_quiz():
    section_id = int(request.args.get('section_id', None))
    time_limit = int(request.args.get('time_limit', None))
    da = Quiz(section_id, time_limit)
    status = da.create_quiz()
    return status
    
@app.route("/get_quiz_questions", methods=['GET'])
def get_quiz_questions():
    quiz_id = int(request.args.get('quiz_id', None))
    da = Quiz()
    questions = da.get_quiz_questions(quiz_id)
    return questions

# @app.route("/create_quiz_questions", methods=['GET'])
# def create_quiz_questions():
#     quiz_id = int(request.args.get('quiz_id', None))
#     question_type = str(request.args.get('quiz_id', None))
#     qorder = str(request.args.get('qorder', None))
#     question =str(request.args.get('question', None))
#     da = SectionMaterialQuizController()
#     status = da.create_quiz_questions(quiz_id,question_type,qorder,question)
#     return status

# @app.route("/view_quiz_questions", methods=['GET'])
# def get_qn():
#     qn_id = int(request.args.get('qn_id', None))
#     da =  SectionMaterialController()
#     quiz = da.view_qn(qn_id)
#     return quiz

@app.route("/create_section_materials", methods=['GET'])
def create_section_materials():
    section_id = int(request.args.get('section_id', None))
    material_title = str(request.args.get('material_title', None))
    material_content = str(request.args.get('material_content', None))
    material_type = str(request.args.get('material_type', None))
    da = SectionMaterials(section_id, material_title, material_content, material_type)
    status = da.create_material()
    return status

'''
Routes of section_quiz_controler - ADD THIS LATER THERE ARE SOME MAJOR ISSUES
'''    
# @app.route("/get_quiz_questions", methods=['GET'])
# def get_quiz_questions():
#     quiz_id = int(request.args.get('quiz_id', None))
#     da = SectionQuizController()
#     status = da.get_quiz_questions(quiz_id)
#     return status

@app.route("/view_quiz_questions", methods=['GET'])
def get_qn():
    qn_id = int(request.args.get('qn_id', None))
    da = TrueFalse()
    questions = da.get_quiz_questions(qn_id)
    return questions

@app.route("/create_TrueFalse", methods=['GET', 'POST'])
def create_TrueFalse():
    answer = int(request.args.get('answer', None))
    quiz_id = int(request.args.get('quiz_id', None))
    qorder = int(request.args.get('qorder', None))
    question_type = str(request.args.get('question_type', None))
    question = str(request.args.get('question', None))
    print(answer)
    da = TrueFalse(quiz_id, answer, qorder, question_type, question)
    status = da.create_TrueFalse()
    return status

@app.route("/create_MCQ_Question", methods=['GET'])
def create_MCQ():
    quiz_id = int(request.args.get('quiz_id', None))
    qorder = int(request.args.get('qorder', None))
    question_type = str(request.args.get('question_type', None))
    question = str(request.args.get('question', None))
    da = QuizQuestions(quiz_id, question_type, qorder, question)
    status = da.create_MCQ()
    return status

@app.route("/add_MCQ_Options", methods=['GET'])
def add_MCQ_options():
    question_id = int(request.args.get('question_id', None))
    option_order = int(request.args.get('option_order', None))
    option_content = str(request.args.get('option_content', None))
    correct_option = int(request.args.get('correct_option',None))
    print('controller option',correct_option)
    da = multiplechoiceoptions(question_id,option_order,option_content,correct_option)
    status = da.create_MCQ_options()
    
    return status 

@app.route("/get_Quiz_Questions_Options", methods=['GET'])
def get_Quiz_Questions():
    quiz_id = int(request.args.get('quiz_id', None))
    da = Quiz()
    questions = da.get_quiz_questions(quiz_id)
    return questions

@app.route("/get_MCQ", methods=['GET'])
def get_MCQ():
    question_id = int(request.args.get('question_id', None))
    da = QuizQuestions()
    questions = da.get_mcq_question_options(question_id)
    return questions

@app.route("/get_TrueFalse", methods=['GET'])
def get_TrueFalse():
    question_id = int(request.args.get('question_id', None))
    da = TrueFalse()
    questions = da.get_quiz_questions(question_id)
    return questions

@app.route("/delete_quiz", methods=['GET'])
def delete_Questions():
    quiz_id = int(request.args.get('quiz_id', None))
    da = Quiz()
    status = da.delete_Quiz(quiz_id)
    return status

@app.route("/submitScore", methods=['POST'])
def submitScore():
    quiz_id = int(request.args.get('quiz_id', None))
    user_id = int(request.args.get('user_id', None))
    quiz_score = float(request.args.get('score', None))
    print(quiz_id, file=sys.stderr)
    print(user_id, file=sys.stderr)
    print(quiz_score, file=sys.stderr)
    scoreObj = {"quiz_id" : quiz_id, "user_id" : user_id, "quiz_score" : quiz_score}
    

    #Check if quiz is graded or not
    finalDA = FinalQuiz()
    gradedOrNot = finalDA.is_graded(quiz_id)

    if(gradedOrNot == False):
        ungradedDa = Ungraded_quiz_score()
        message = ungradedDa.insert_score(scoreObj)
        return message
    else:
        gradedDa = Graded_quiz_score()
        if float(quiz_score) >= float(gradedOrNot[0]):
            scoreObj["result"] = True
        else:
            scoreObj["result"] = False
        
        message = gradedDa.insert_score(scoreObj)
        return message

@app.route("/get_Quiz_Timer", methods=['GET'])
def get_quiz_timer():
    quiz_id = int(request.args.get('quiz_id', None))
    da = Quiz()
    timer = da.get_time_limit_with_id(quiz_id)
    return timer

@app.route("/get_Section_Title", methods=['GET'])
def get_section_title():
    quiz_id = int(request.args.get('quiz_id', None))
    qa = Quiz()
    section_id = qa.get_section_id_with_quiz_id(quiz_id)
    da = Section()
    quiz_title = da.get_section_title_with_id(section_id)
    
    return quiz_title

'''
Routes of view_controller
'''
@app.route("/eligible_courses", methods=['POST'])
def get_eligible_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_eligible_courses(user_id)
    courses = record[0]
    classes = record[1]
    final_list = []
    for i in range(len(courses)):
        course_info = courses[i].json()
        class_info = classes[i].json()
        course_info.update(class_info)
        final_list.append(course_info)

    if len(final_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "record": [a_record for a_record in final_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no eligible courses."
            }
        ), 404

@app.route("/eligible_classes", methods=['POST'])
def get_eligible_classes():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_eligible_classes(user_id)
    courses = record[0]
    classes = record[1]
    final_list = []
    for i in range(len(courses)):
        course_info = courses[i].json()
        class_info = classes[i].json()
        course_info.update(class_info)
        final_list.append(course_info)

    if len(final_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "record": [a_record for a_record in final_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no eligible classes."
            }
        ), 404

@app.route("/uneligible_courses", methods=['POST'])
def get_uneligible_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_uneligible_courses(user_id)
    if len(record):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "record": [a_record.json() for a_record in record]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no uneligible courses."
            }
        ), 404

@app.route("/enrolled_classes", methods=["POST"])
def get_enrolled_course_class():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_enrolled_course_class(user_id)
    courses = record[0]
    classes = record[1]
    final_list = []
    for i in range(len(courses)):
        course_info = courses[i].json()
        class_info = classes[i].json()
        course_info.update(class_info)
        final_list.append(course_info)

    if len(final_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "record": [a_record for a_record in final_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no enrolled classes."
            }
        ), 404

@app.route("/assigned_courses", methods=['POST'])
def get_assigned_course_class():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_assigned_course_class(user_id)
    courses = record[0]
    classes = record[1]
    final_list = []
    for i in range(len(courses)):
        course_info = courses[i].json()
        class_info = classes[i].json()
        course_info.update(class_info)
        final_list.append(course_info)
        
    if len(final_list):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "record": [a_record for a_record in final_list]
                    }
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "There are no assigned courses."
            }
        ), 404

@app.route("/completed_courses", methods=['POST'])
def get_completed_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_completed_courses(user_id)
    if len(record):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "record": [a_record.json() for a_record in record]
                    }
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "There are no completed courses."
            }
        ), 404

@app.route("/get_all_learner_id",methods = ['GET'])
def get_all_learner_ids():
    lrnr = Learner()
    records = lrnr.get_all_learners_id()
    return records

@app.route("/get_all_learners",methods = ['GET'])
def get_all_learner():
    lrnr = Learner()
    record = lrnr.get_all_learners()
    if len(record):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "record": [a_record.json() for a_record in record]
                    }
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "There are no learners."
            }
        ), 404

@app.route("/get_courses_with_classes_without_trainer",methods = ['GET'])
def get_courses_with_classes_without_trainer():
    record = ViewController.get_courses_with_classes_without_trainer()
    if len(record):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "record": [a_record.json() for a_record in record]
                    }
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "There are no classes without a trainer"
            }
        ), 404

@app.route("/get_classes_of_a_course_without_trainer",methods = ['POST'])
def get_classes_of_a_course_without_trainer():
    application = request.get_json()
    c_id = application['course_id']
    
    record = ViewController.get_classes_of_a_course_without_trainer(c_id)
    
    # return record
    if len(record):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "record": [a_record.json() for a_record in record]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no classes without a trainer"
            }
        ), 404

@app.route("/get_all_trainers",methods = ['GET'])
def get_all_trainers():
    trnr = Trainer()
    
    record = trnr.get_all_trainers()
    
    # return record
    if len(record):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "record": [a_record.json() for a_record in record]
                    }
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "There are no classes without a trainer"
            }
        ), 404

@app.route("/get_all_assigned_classes_of_user", methods = ['POST'])
def get_all_assigned_classes_of_user():
    application = request.get_json()
    user_id = application['user_id']
    
    lrnr_class = Learner_Assignment()
    record = lrnr_class.get_user_assigned_courses(user_id)
    course_class = Course()
    
    new_record = []

    for a_record in record:
        print(a_record.get_course_id())
        course_id, class_id = a_record.get_course_id()
        course_rec = course_class.get_course_by_id(course_id)
        course_name = course_rec.get_course_name()
        a_record = {
            "course_id" : course_id,
            "class_id" : class_id,
            "course_name" : course_name
        }
        new_record.append(a_record)

    if len(record):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "record": [a_record for a_record in new_record]
                    }
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "There are no assigned classes"
            }
        ), 404

@app.route("/get_all_enrolled_classes_of_user", methods = ['POST'])
def get_all_enrolled_classes_of_user():
    application = request.get_json()
    # print(application)
    user_id = application['user_id']
    
    crse_enrol_class = Course_Enrollment()
    record = crse_enrol_class.get_user_enrolled_courses(user_id)
    course_class = Course()
    
    new_record = []

    for a_record in record:
        course_id,class_id = a_record.get_course_and_class_id()
        course_rec = course_class.get_course_by_id(course_id)
        course_name = course_rec.get_course_name()
        a_record = {
            "course_id" : course_id,
            "class_id" : class_id,
            "course_name" : course_name
        }
        new_record.append(a_record)
        

    if len(record):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "record": [a_record for a_record in new_record]
                    }
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "There are no enrolled classes"
            }
        ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)


from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from course_enrollment import Course_Enrollment
from learner_badges import learnerbadges
from course_prerequisites import Course_Prerequisites
from classes import Classes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class EnrollmentController():
    def apply_class(self, application):
        userid = application['user_id']
        class_id = application['class_id']
        course_id = application['course_id']
        is_enrolled = 0

        # check if fulfilled prerequisites
        completed_courses = learnerbadges()
        course_prereq = Course_Prerequisites()
        fulfilled_prereq = completed_courses.get_completed_courses(userid)
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
        

@app.route("/enroll", methods=['POST'])
def apply_class():
    application = request.get_json()
    enroll_ctrl = EnrollmentController()
    return enroll_ctrl.apply_class(application)

if __name__ == '__main__':
    app.run(port=5010, debug=True)
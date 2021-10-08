from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from  course_enrollment_data_access import CourseEnrollmentDataAccess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class courseEnrollmentController():
    def retrieveAllEnrollment(self):
        enrollmentDA = CourseEnrollmentDataAccess()
        enrollments = enrollmentDA.retrieveAllEnrollments()
        return enrollments

    def changeEnrollmentStatus(self, enrollment_id):
        enrollmentDA = CourseEnrollmentDataAccess()
        output = enrollmentDA.changeEnrollmentStatus(enrollment_id)
        return output
# #   View all materials in a section
#     def view_all_materials(self,section_id):
#         da = SectionMaterialQuizDataAccess()
#         materials = da.get_material_record_by_section(section_id)
#         return materials


#   Download Course Materials
    #tbu after initializing S3

        


############## View Functions ###############################
@app.route("/allEnrollments", methods=['GET'])
def getAllEnrollments():
    da = courseEnrollmentController()
    enrollments = da.retrieveAllEnrollment()
    return enrollments

@app.route("/changeEnrollmentStatus/input")
def changeEnrollStatus():
    da = courseEnrollmentController()
    enrollId = int(request.args.get('enrol_id', None))
    output = da.changeEnrollmentStatus(enrollId)
    return output



if __name__ == '__main__':
    app.run(port=5005, debug=True)
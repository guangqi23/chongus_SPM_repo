from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

# flask implementation
class Course(db.Model):
    __tablename__ = 'course'

    # this is equivalent to the __init__ statement for classes but a flask implementation of it
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.String(300), nullable=False)
    startdate = db.Column(db.DateTime, nullable=False)
    enddate = db.Column(db.DateTime, nullable=False)
    startenrollmentdate = db.Column(db.DateTime, nullable=False)
    endenrollmentdate = db.Column(db.DateTime, nullable=False)
    prerequisites = []

    def add_prerequisites(self, course_id, prereq):
        self.prerequisites.append(course_id, prereq)

    def get_all_courses():
        return Course.query.all()

    def get_course_by_id(self, course_id):
        record = Course.query.filter_by(course_id=course_id).first()
        return record

    def add_course(self):
        # this should check if there is already an existing course in the database. To be added later
        try: 
            db.session.add(self)
            db.session.commit()
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

    def del_course(self, course_id):
        course = self.query.filter_by(course_id=course_id).first()
        try: 
            db.session.delete(course)
            db.session.commit()
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
   
    def json(self):
        return {"course_id": self.course_id, "course_name": self.course_name, "course_description": self.course_description, "startdate": self.startdate, 
                "enddate": self.enddate, "startenrollmentdate": self.startenrollmentdate, "endenrollmentdate": self.endenrollmentdate}   

class Course_Prerequisites(db.Model):
    __tablename__ = 'course_prerequisites'

    course_id = db.Column(db.Integer, primary_key=True)
    prereq_course_id = db.Column(db.Integer, primary_key=True)

    def add_prereq(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            return jsonify(
                {
                    "code": 500,
                    "message": "There was an error when adding the prerequisite. " + str(error)
                }
            )
        
        return jsonify(
            {
                "code": 200,
                "message": "The prerequisite has been successfully added"
            }
        ), 200
    
   def json(self):
        return {"course_id": self.course_id, "prereq_course_id": self.prereq_course_id}
    
    def prereq_by_course(self,course_id):
        record = Course_Prerequisites.query.filter_by(course_id=course_id).all()
        return record

@app.route("/prerequisitesbycourse", methods=['POST'])
def prereq_by_course():
    application = request.get_json()
    user_id = application['course_id']
    prereq = Course_Prerequisites()
    record = prereq.prereq_by_course(user_id)
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

if __name__ == '__main__':
    app.run(port=5003, debug=True)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
#from flask_cors import CORS
app = Flask(__name__)

# Database Configuration
# Database - customer configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
dbc = SQLAlchemy(app)
#Priority
#Customer->Restaurant->Reservation->Menu->Preorder->Notifications
#Customer DB configuration
class COURSE(dbc.Model):
    __tablename__ = 'COURSE'

    COURSE_ID = dbc.Column(dbc.String(64), primary_key=True)
    COURSE_NAME = dbc.Column(dbc.String(64), nullable=False)
    COURSE_DESCRIPTION = dbc.Column(dbc.String(255), nullable=False)
    STARTDATE = dbc.Column(dbc.DateTime, nullable=False)
    ENDDATE = dbc.Column(dbc.DateTime, nullable=False)
    STARTENROLLMENTDATE = dbc.Column(dbc.DateTime, nullable=True)
    ENDENROLLMENTDATE= dbc.Column(dbc.DateTime, nullable=True)

    def __init__(self, COURSE_ID, COURSE_NAME, COURSE_DESCRIPTION, STARTDATE, ENDDATE,STARTENROLLMENTDATE,ENDENROLLMENTDATE):
        self.COURSE_ID = COURSE_ID
        self. COURSE_NAME = COURSE_NAME
        self.COURSE_DESCRIPTION = COURSE_DESCRIPTION
        self.STARTDATE = STARTDATE
        self.ENDDATE = ENDDATE
        self.STARTENROLLMENTDATE = STARTENROLLMENTDATE
        self.ENDENROLLMENTDATE = ENDENROLLMENTDATE

    def json(self):
        return {"COURSE_ID": self.COURSE_ID, "COURSE_NAME": self.COURSE_NAME, "COURSE_DESCRIPTION": self.COURSE_DESCRIPTION, "STARTDATE": self.STARTDATE, "ENDDATE": self.ENDDATE,"STARTENROLLMENTDATE": self.STARTENROLLMENTDATE,"STARTENROLLMENTDATE": self.STARTENROLLMENTDATE}

# Routes to to be added1
@app.route("/")
def home():
    return "If you see this message,it is working"
####################################################################################################################################################################

#Customer Functions

####################################################################################################################################################################
# Customer: return all customers
@app.route("/ALL_COURSES")
def get_all():
    # capital C, you are calling a class created above
    courseList =COURSE.query.all()
    if len(courseList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "COURSE": [COURSE.json() for course in courseList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no customers."
        }
    ), 404


####################################################################################################################################################################
# Dont edit what is after this
if __name__ == '__main__':
    app.run(port=5000, debug=True)
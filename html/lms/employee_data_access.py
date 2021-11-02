from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from user import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

# shouldnt be used anymore
class EmployeeDataAccess():
    def validate_hr(self, user_id):
        user = User()
        is_hr = user.is_hr(user_id)
    
        # check employee_id is in hr_ids
        if is_hr:
            return jsonify(
                    {
                        "code": 200,
                        "message": "user id is belongs to a valid HR"
                    }
                )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "user id does not belong to a valid HR"
                }
            ), 404

    def validate_qualifications():
        pass

    def validate_prerequisites():
        pass
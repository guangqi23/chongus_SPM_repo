from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.sql.expression import false, true

from learner import Learner

app = Flask(__name__)
CORS(app) 

class ViewController():
    pass

@app.route("/eligible_courses", methods=['POST'])
def get_eligible_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_eligible_courses(user_id)
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
            "message": "There are no eligible courses."
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
    
@app.route("/enrolled_courses", methods=['POST'])
def get_enrolled_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_enrolled_courses(user_id)
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
            "message": "There are no enrolled courses."
            }
        ), 404

@app.route("/enrolled_classes", methods=["POST"])
def get_enrolled_classes():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_enrolled_classes(user_id)
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
            "message": "There are no enrolled classes."
            }
        ), 404


@app.route("/assigned_courses", methods=['POST'])
def get_assigned_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner = Learner()
    record = learner.get_assigned_courses(user_id)
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
            "message": "There are no assigned courses."
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
            "message": "There are no assigned courses."
            }
        ), 404
    

if __name__ == '__main__':
    app.run(port=5002, debug=True)
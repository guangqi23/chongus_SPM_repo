from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from classes import Classes
import sys
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:wangxingjie@spmdatabase.ca0m2kswbka0.us-east-2.rds.amazonaws.com:3306/LMSDB2'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lmsdb'



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

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



if __name__ == '__main__':
    app.run(port=5011, debug=True)
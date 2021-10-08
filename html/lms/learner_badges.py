from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/lmsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class learnerbadges(db.Model):
    __tablename__ = 'learner_badges'

    userid = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, primary_key=True)

    def json(self):
        return {"user_id": self.userid, "course_id": self.course_id}

    def get_completed_courses(self, userid):
        record = learnerbadges.query.filter_by(userid=userid).all()
        return record

@app.route("/learnerbadges", methods=['POST'])
def get_completed_courses():
    application = request.get_json()
    user_id = application['user_id']
    learner_badges = learnerbadges()
    record = learner_badges.get_completed_courses(user_id)
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


if __name__ == '__main__':
    app.run(port=5001, debug=True)

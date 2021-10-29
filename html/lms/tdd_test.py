import unittest
from flask.json import jsonify
import requests
from course_controller import CourseController

class TestCourseController(unittest.TestCase):
    def test_create_course(self):
        api_url = "http://127.0.0.1:5000/create_course"
        application = {
            "user_id": "1",
            "course_name": "test_name",
            "course_description": "testing",
            "start_enrollment_date": "2020-01-01 00:00:00",
            "end_enrollment_date": "2020-01-01 00:00:00"
        }

        r = requests.post(api_url, json=application)
        self.assertEqual(r.status_code, 200)

    def test_delete_course(self):
        api_url = "http://127.0.0.1:5000/delete_course"
        application = {
            "user_id": "1",
            "course_id": "8",
        }
        r = requests.post(api_url, json=application)
        self.assertEqual(r.status_code, 200)


    def test_change_enrollment_status(self):
        api_url = "http://localhost:5000/changeEnrollmentStatus/input?enrol_id=1"
        r = requests.get(api_url)
        self.assertEqual(r.status_code, 200)

    def test_retrieve_enrollment_status(self):
        api_url = "http://127.0.0.1:5000/allEnrollmentsPending"

        r = requests.get(api_url)
        self.assertEqual(r.status_code, 200)
    

# https://www.youtube.com/watch?v=iQVvpnRYl-w
if __name__ == "__main__":
    unittest.main()
import unittest
import requests

class TestCourseController(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/create_course"
    application = {
        "user_id": "1",
        "course_name": "test_name",
        "course_description": "testing",
        "start_date": "2020-01-01 00:00:00",
        "end_date": "2020-01-01 00:00:00",
        "start_enrollment_date": "2020-01-01 00:00:00",
        "end_enrollment_date": "2020-01-01 00:00:00"
    }

    def test_create_course(self):
        r = requests.post(TestCourseController.API_URL, json=TestCourseController.application)
        self.assertEqual(r.status_code, 200)

if __name__ == "__main__":
    unittest.main()
import unittest
from flask import json
from flask.json import jsonify
import requests



class test_AssignController(unittest.TestCase):




    def test_assign_trainer(self):

        assign_url = 'http://127.0.0.1:5001/assign_course_trainer'
        application = {
            "class_id" : '1',
            "course_id" : "3",
            'hr_id' : '3',
            'trainer_id' : '2'
        }
        
        r = requests.post(assign_url, json=application)
        self.assertEqual(r.status_code, 200)

    


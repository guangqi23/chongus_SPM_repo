import unittest
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
import re
from course import COURSE
from course import app
from unittest import TestCase
#from flask_cors import CORS



class FlaskTest(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/ALL_COURSES")
        statuscode = response.status_code
        self.assertEqual(statuscode,200)



#https://www.youtube.com/watch?v=UZyZw4tYJMI
if __name__ == '__main__':
    unittest.main()

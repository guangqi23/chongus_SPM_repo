import unittest
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
import re
from SectionMaterialController import app
#from unittest import TestCase
#from flask_cors import CORS



class FlaskTest(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("http://localhost:5001/view_section_materials?section_id=0")
        #raise exception if section id =0; else pass.
        statuscode = response.status_code
        self.assertEqual(statuscode,200)


#https://www.youtube.com/watch?v=UZyZw4tYJMI
if __name__ == '__main__':
    unittest.main()

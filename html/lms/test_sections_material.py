import unittest
from flask import json
from flask.json import jsonify
import flask_testing
from flask_sqlalchemy import SQLAlchemy
from app import *
from app import app,db


#Coded by: Wang Xing Jie

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    db.init_app(app)

    def create_app(self):
        return app
    
    def setUp(self):
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()


class test_Sections_Materials(unittest.TestCase):


    def test_get_material_id(self):
        material = SectionMaterials(
            material_id = '7',
            section_id = '3',
            material_title = "Test material title",
            material_content = "https://happybucket7.s3.amazonaws.com/6715758.pdf?AWSAccessKeyId=ASIATQE7K7S4UEVS6Y5E",
            material_type = "pdf"
        )

        self.assertEqual(material.get_material_id(), '7')
    
    def test_get_section_id(self):
        material = SectionMaterials(
            material_id = '7',
            section_id = '3',
            material_title = "Test material title",
            material_content = "https://happybucket7.s3.amazonaws.com/6715758.pdf?AWSAccessKeyId=ASIATQE7K7S4UEVS6Y5E",
            material_type = "pdf"
        )

        self.assertEqual(material.get_section_id(), '3')
    
    def test_get_section_material_title(self):
        material = SectionMaterials(
            material_id = '7',
            section_id = '3',
            material_title = "Test material title",
            material_content = "https://happybucket7.s3.amazonaws.com/6715758.pdf?AWSAccessKeyId=ASIATQE7K7S4UEVS6Y5E",
            material_type = "pdf"
        )

        self.assertEqual(material.get_section_material_title(), 'Test material title')
    
    def test_get_section_material_content(self):
        material = SectionMaterials(
            material_id = '7',
            section_id = '3',
            material_title = "Test material title",
            material_content = "https://happybucket7.s3.amazonaws.com/6715758.pdf?AWSAccessKeyId=ASIATQE7K7S4UEVS6Y5E",
            material_type = "pdf"
        )

        self.assertEqual(material.get_section_material_content(), 'https://happybucket7.s3.amazonaws.com/6715758.pdf?AWSAccessKeyId=ASIATQE7K7S4UEVS6Y5E')

    def test_get_section_material_type(self):
        material = SectionMaterials(
            material_id = '7',
            section_id = '3',
            material_title = "Test material title",
            material_content = "https://happybucket7.s3.amazonaws.com/6715758.pdf?AWSAccessKeyId=ASIATQE7K7S4UEVS6Y5E",
            material_type = "pdf"
        )

        self.assertEqual(material.get_section_material_type(), 'pdf')


class test_sections_material_controller(TestApp):

    def test_get_materials_individual(self):
        material = SectionMaterials(
            material_id = '7',
            section_id = '3',
            material_title = "Test material title",
            material_content = "https://happybucket7.s3.amazonaws.com/6715758.pdf?AWSAccessKeyId=ASIATQE7K7S4UEVS6Y5E",
            material_type = "pdf"
        )

        db.session.add(material)
        db.session.commit()

        testMaterial = SectionMaterials()
        material_id = 7
        section_id = 3
        result = testMaterial.get_materials_individual(material_id, section_id)
        self.assertIsNotNone(result)

    
    def test_create_material(self):
       
        section_id = '3',
        material_title = "Test material title",
        material_content = "https://happybucket7.s3.amazonaws.com/6715758.pdf?AWSAccessKeyId=ASIATQE7K7S4UEVS6Y5E",
        material_type = "pdf"
        
        testSectionMaterial = SectionMaterials()
        result = testSectionMaterial.create_material(section_id, material_title, material_content, material_type)
        print(result[1])
        self.assertEqual(json.loads(result[0].data), 200)



if __name__ == '__main__':
    unittest.main()
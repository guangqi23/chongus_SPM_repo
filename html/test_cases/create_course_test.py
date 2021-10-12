import unittest
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
import re
from lms.course import COURSE
from lms.course import app
from unittest import TestCase
#from flask_cors import CORS
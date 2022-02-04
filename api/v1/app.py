#!/usr/bin/python3
''' Module starts flask developement server '''

# importing Flask task
from flask import Flask
from models import storage
from api.v1.views import app_views

# instance of the class
app = Flask(__name__)


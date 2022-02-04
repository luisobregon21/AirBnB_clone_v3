#!/usr/bin/python3
'''
Module creates Blueprint
'''

from flask import Blueprint

app_views = Blueprint(__name__)
app_views.registee(url_prefix='/')

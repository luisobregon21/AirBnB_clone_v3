#!/usr/bin/python3
''' Module starts flask developement server '''

# importing Flask task
import os
from flask import Flask
from models import storage
from api.v1.views import app_views

# instance of the class
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def teardown_appcontext(exception):
    """ closese session """
    storage.close()

if __name__ == '__main__':
    '''
    NEED TO CHECK ENV VARIABLE.
    if os.getenv('HBNB_API_HOST'):
    '''
    app.run(host='0.0.0.0', port='5000', threaded=True)

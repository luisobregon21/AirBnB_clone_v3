#!/usr/bin/python3
'''Module creates instance of flask'''


from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def handler(exception):
    '''Method calls storage.close() method'''
    storage.close()


if __name__ == "__main__":
#    api_host = getenv('HBNB_API_HOST')
#    api_port = getenv('HBNB_API_PORT')
#    app.run(host=api_host, port=api_port, threaded=True)
    try:
        host = getenv("HBNB_API_HOST")
    except:
        host = "0.0.0.0"
    try:
        port = getenv("HBNB_API_PORT")
    except:
        port = "5000"
    app.run(host=host, port=port, threaded=True)

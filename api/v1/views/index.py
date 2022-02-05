#!/usr/bin/python3
'''Module creates route /status on object app_views'''


from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route('stats', strict_slashes=False)
def stats():

    cls_dic = {"Amenity": "amenities", "City": "cities", "Place": "places",
               "Review": "reviews", "State": "states", "User": "users"}
    all_obj = {}

    for key, value in cls_dic.items():
        count = storage.count(key)
        all_obj[value] = count
    return jsonify(all_obj)


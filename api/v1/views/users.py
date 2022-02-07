#!/usr/bin/python3
'''Users objects handles all default RESTful API actions'''


from flask import jsonify, request, abort
from itsdangerous import json
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_users():
    if request.method == 'POST':
        new_user = None
        try:
            request_dict = request.get_json()
            user_email = request_dict.get('email')
            if user_email is None:
                abort(400, description='Missing email')
            user_pw = request_dict.get('password')
            if user_pw is None:
                abort(400, description='Missing password')
            new_user.save()
            return jsonify(new_user.to_dict()), 201
        except:
            abort(400, description='Not a JSON')

    all_users = storage.all('User')
    user_list = []
    for user in all_users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def user_by_id(user_id):
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            request_dict = request.get_json()
            request_dict['id'] = user.id
            request_dict['email'] = user.email
            request_dict['created_at'] = user.created_at
            request_dict['updated_at'] = user.updated_at
            user.__init__(**request_dict)
            user.save()
            return jsonify(user.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(user.to_dict())

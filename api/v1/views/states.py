#!/usr/bin/python3
'''
State objects that handles all default RESTFul API actions
'''


from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['POST', 'GET'], strict_slashes=False)
def all_States():
    if request.method == 'POST':
        new_state = None
        try:
            request_dict = request.get_json()
            state_name = request_dict.get('name')
            if state_name is None:
                abort(400, description='Missing name')
            new_state = State(name=state_name)
            new_state.save()
            return jsonify(new_state.to_dict()), 201
        except:
            abort(400, description='Not a JSON')

    # Retrieving all State objects
    all_states = storage.all('State')
    state_list = []
    for state in all_states.values():
        state_list.append(state.to_dict())
    # returning all states in a list
    return jsonify(state_list)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def state_by_id(state_id):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            request_dict = request.get_json()
            request_dict['id'] = state.id
            request_dict['created_at'] = state.created_at
            state.__init__(**request_dict)
            state.save()
            return jsonify(state.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(state.to_dict())

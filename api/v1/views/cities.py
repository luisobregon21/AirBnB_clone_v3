#!/usr/bin/python3
'''
city objects that handles all default RESTFul API actions
'''


from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['POST', 'GET'],
                 strict_slashes=False)
def all_cities(state_id):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if request.method == 'POST':
        new_city = None
        try:
            request_dict = request.get_json()
            city_name = request_dict.get('name')
            if city_name is None:
                abort(400, description='Missing name')
            new_city = City(name=city_name, state_id=state_id)
            new_city.save()
            return jsonify(new_city.to_dict()), 201
        except:
            abort(400, description='Not a JSON')

    # Retrieving all city objects
    city_list = []
    for city in state.cities:
        city_list.append(city.to_dict())
    # returning all citys in a list
    return jsonify(city_list)


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def city_by_id(city_id):
    city = storage.get('city', city_id)
    if city is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            request_dict = request.get_json()
            request_dict['id'] = city.id
            request_dict['created_at'] = city.created_at
            city.__init__(**request_dict)
            city.save()
            return jsonify(city.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(city.to_dict())

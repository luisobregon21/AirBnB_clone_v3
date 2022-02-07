#!/usr/bin/python3
'''Places objects handles all default RESTful API actions'''


from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_places(city_id):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if request.method == 'POST':
        new_place = None
        try:
            request_dict = request.get_json()
            place_name = request_dict.get('name')
            if place_name is None:
                abort(400, description='Missing name')
            new_place = Place(name=place_name, city_id=city_id)
            new_place.save()
            return jsonify(new_place.to_dict()), 201
        except:
            abort(400, description='Not a JSON')

#    Retrieving all place objects
    place_list = []
    for places in city:
        place_list.append(places.to_dict())
#    Returns all places in a list
    return jsonify(place_list)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place_by_id(place_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            request_dict = request.get_json()
            request_dict['id'] = place.id
            request_dict['created_at'] = place.created_at
            place.__init__(**request_dict)
            place.save()
            return jsonify(place.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(place.to_dict)

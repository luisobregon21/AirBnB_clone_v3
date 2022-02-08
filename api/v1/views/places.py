#!/usr/bin/python3
'''Places objects handles all default RESTful API actions'''


from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def all_places(city_id):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if request.method == 'POST':
        new_places = None
        try:
            request_dict = request.get_json()
            user_id = request_dict.get('user_id')
            if user_id is None:
                abort(400, description='Missing user_id')
            user = storage.get('User', request_dict['user_id'])
            if user is None:
                abort(404)
            place_name = request_dict.get('name')
            if place_name is None:
                abort(400, 'Missing name')
            new_places = Place(user_id=user_id, city_id=city_id,
                               name=place_name)
            new_places.save()
            return jsonify(new_places.to_dict()), 201
        except:
            abort(400, description='Not a JSON')

    all_places = storage.all('Place')
    places_list = []
    for places in all_places.values():
        places_list.append(places.to_dict())
    return jsonify(places_list)


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
            request_dict['user_id'] = place.user_id
            request_dict['city_id'] = place.city_id
            request_dict['created_at'] = place.created_at
            request_dict['updated_at'] = place.updated_at
            place.__init__(**request_dict)
            place.save()
            return jsonify(place.to_dict())
        except:
            abort(400, description='Not a JSON')
    return jsonify(place.to_dict())

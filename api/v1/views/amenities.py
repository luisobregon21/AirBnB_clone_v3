#!/usr/bin/python3
'''
Amenity objects that handles all default RESTFul API actions
'''


from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['POST', 'GET'],
                 strict_slashes=False)
def all_Amenities():
    if request.method == 'POST':
        new_amenity = None
        try:
            request_dict = request.get_json()
            amenity_name = request_dict.get('name')
            if amenity_name is None:
                abort(400, description='Missing name')
            new_amenity = Amenity(name=amenity_name)
            new_amenity.save()
            return jsonify(new_amenity.to_dict()), 201
        except:
            abort(400, description='Not a JSON')

    # Retrieving all Amenity objects
    all_amenities = storage.all('Amenity')
    amenity_list = []
    for amenity in all_amenities.values():
        amenity_list.append(amenity.to_dict())
    # returning all amenities in a list
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenities_by_id(amenity_id):
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            request_dict = request.get_json()
            request_dict['id'] = amenity.id
            request_dict['created_at'] = amenity.created_at
            amenity.__init__(**request_dict)
            amenity.save()
            return jsonify(amenity.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(amenity.to_dict())

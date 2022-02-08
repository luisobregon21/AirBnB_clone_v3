#!/usr/bin/python3
'''reviews objects handles all default RESTful API actions'''


from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/cities/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_reviews(place_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if request.method == 'POST':
        new_review = None
        try:
            request_dict = request.get_json()
            review_txt = request_dict.get('text')
            if review_txt is None:
                abort(400, description='Missing txt')
        except:
            abort(400, description='Not a JSON')
        review_user = request_dict.get('user_id')
        if review_user is None:
            abort(400, description='Missing user_id')
        user = storage.get('User', review_user)
        if user is None:
            abort(404)
        new_review = Review(name=review_txt, place_id=place_id,
                          user_id=review_user)
        new_review.save()
        return jsonify(new_review.to_dict()), 201

#    Retrieving all review objects
    review_list = []
    for reviews in place.review:
        review_list.append(reviews.to_dict())
#    Returns all reviews in a list
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def review_by_id(review_id):
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            request_dict = request.get_json()
            request_dict['id'] = review.id
            request_dict['place_id'] = review.place_id
            request_dict['created_at'] = review.created_at
            request_dict['user_id'] = review.user_id
            review.__init__(**request_dict)
            review.save()
            return jsonify(review.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(review.to_dict())

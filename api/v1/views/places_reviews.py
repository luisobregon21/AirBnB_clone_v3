#!/usr/bin/python3
'''reviews objects handles all default RESTful API actions'''


from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_reviews(place_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if request.method == 'POST':
        new_review = None
        request_dict = None
        try:
            request_dict = request.get_json()
            new_review = request_dict.get('text')
        except:
            abort(400, description='Not a JSON')
        review_user = request_dict.get('user_id')
        if review_user is None:
            abort(400, description='Missing user_id')
        user = storage.get('User', review_user)
        if user is None:
            abort(404)
        if new_review is None:
            abort(400, description='Missing txt')
        the_review = Review(text=new_review, place_id=place_id,
                            user_id=review_user)
        the_review.save()
        return jsonify(the_review.to_dict()), 201

#    Retrieving all review objects
    review_list = []
    for reviews in place.reviews:
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
            request_dict['created_at'] = review.created_at
            try:
                request_dict.pop('user_id', None)
                request_dict.pop('place_id', None)
            except:
                pass
            review.__init__(**request_dict)
            review.save()
            return jsonify(review.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(review.to_dict())

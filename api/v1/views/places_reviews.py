#!/usr/bin/python3
"""
Reviews endpoints
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"])
def review_by_place_id(place_id):
    """retrieve  place objects from storage by review id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == "POST":
        data = request.get_json(silent=True)

        if data is None:
            abort(400, 'Not a JSON')

        if user_id is None:
            abort(400, 'Missing user_id')

        user_id = data.get("user_id")
        if storage.get(User, user_id) is None:
            abort(404)

        if data.get("text") is None:
            abort(400, 'Missing text')

        new_review = Review(**data)
        new_review.place_id = place_id
        new_review.user_id = user_id
        new_review.save()
        return jsonify(new_review.to_dict()), 201

    review_list = [review.to_dict() for review in place.reviews]
    return jsonify(review_list), 200


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"])
def get_delet_update_reviews(review_id):
    """retrieve, update or delete a place objects from storage by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        keys = ["id", "user_id", "place_id", "created_at", "updated_at"]

        for key, value in data.items():
            if key not in keys:
                setattr(review, key, value)
        storage.save()

    return jsonify(review.to_dict()), 200

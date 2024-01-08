#!/usr/bin/python3
"""
Reviews endpoints
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models import storage
from os import getenv


@app_views.route("/places/<place_id>/amenities")
def amenities_by_place_id(place_id):
    """retrieve  amenities objects from storage by place id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = place.amenities
    else:
        amenities = place.amenity_ids

    amenity_list = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenity_list), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST", "DELETE"])
def get_create_delete_amenities(place_id, amenity_id):
    """retrieve, create or delete a amenities objects"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)

    if amenity is None:
        abort(404)

    if request.method == "POST":
        if getenv("HBNB_TYPE_STORAGE") == "db":
            if amenity not in place.amenities:
                place.amenities.append(amenity)
        else:
            if amenity_id not in place.amenity_ids:
                place.amenity_ids.append(amenity_id)

        storage.save()
        return jsonify(amenity.to_dict()), 200

    elif request.method == "DELETE":
        if getenv("HBNB_TYPE_STORAGE") == "db":
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)

        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(amenity_id)
        storage.save()
        return jsonify({}), 200

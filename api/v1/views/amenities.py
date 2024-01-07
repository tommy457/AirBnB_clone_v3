#!/usr/bin/python3
"""
Amenities endpoints
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=["GET", "POST"])
def get_create_amenities():
    """retrieve or create amenities objects from storage"""
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None:
            abort(400, "Not a JSON")

        if data.get("name") is None:
            abort(400, "Missing name")

        new_amenity = Amenity(**data)
        new_amenity.save()

        return jsonify(new_amenity.to_dict()), 201

    amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in amenities]

    return jsonify(amenities_list), 200


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"])
def get_delete_update_amenities_id(amenity_id):
    """retrieve, delets or updates amenities object from storage by it's id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({})

    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None:
            abort(400, "Not a JSON")
        keys = ["id", "created_at", "updated_at"]

        for key, value in data.items():
            if key not in keys:
                setattr(amenity, key, value)
        storage.save()

    return jsonify(amenity.to_dict()), 200

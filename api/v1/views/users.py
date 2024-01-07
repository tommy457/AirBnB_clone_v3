#!/usr/bin/python3
"""
Amenities endpoints
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage



@app_views.route("/users", methods=["GET", "POST"])
def get_create_users():
    """retrieve or create users objects from storage"""
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None:
            abort(400, "Not a JSON")

        if data.get("email") is None:
            abort(400, "Missing email")

        if data.get("password") is None:
            abort(400, "Missing password")

        new_user = User(**data)
        new_user.save()

        return jsonify(new_user.to_dict()), 201

    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]

    return jsonify(users_list), 200


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"])
def get_delete_update_users_id(user_id):
    """retrieve, delets or updates a users object from storage by it's id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({})

    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None:
            abort(400, "Not a JSON")
        keys = ["id", "email", "created_at", "updated_at"]

        for key, value in data.items():
            if key not in keys:
                setattr(user, key, value)
        storage.save()

    return jsonify(user.to_dict()), 200

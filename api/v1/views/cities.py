#!/usr/bin/python3
"""
Cities endpoints
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def city_by_state_id(state_id):
    """retrieve  city objects from storage by state id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')

        if data.get("name") is None:
            abort(400, 'Missing name')
        new_city = City(**data)
        new_city.state_id = state_id
        new_city.save()
        return jsonify(new_city.to_dict()), 201

    cities_list = [city.to_dict() for city in state.cities]
    return jsonify(cities_list), 200


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def get_delet_update_cities(city_id):
    """retrieve, update or delete a city objects from storage by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        keys = ["id", "created_at", "updated_at"]

        for key, value in data.items():
            if key not in keys:
                setattr(city, key, value)
        storage.save()
    return jsonify(city.to_dict()), 200

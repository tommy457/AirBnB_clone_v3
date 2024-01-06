#!/usr/bin/python3
"""
States endpoints
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET", "POST"])
def get_create_states():
    """retrieve  states objects from storage"""
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")

        if data.get("name") is None:
            abort(400, "Missing name")

        new_state = State(**data)
        new_state.save()

        return make_response(jsonify(new_state.to_dict()), 201)
    if request.method == "GET":
        res = storage.all(State).values()
        states = []
        for state in res:
            states.append(state.to_dict())
        return make_response(jsonify(states), 200)


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def get_delete_update_states_id(state_id):
    """retrieve, delets or updates a state object from storage by it's id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}))

    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        keys = ["id", "created_at", "updated_at"]

        for key, value in data.items():
            if key not in keys:
                setattr(state, key, value)
        storage.save()
        updated_state = state.to_dict()
        return make_response(jsonify(updated_state))

    if request.method == "GET":
        return make_response(jsonify(state.to_dict()), 200)

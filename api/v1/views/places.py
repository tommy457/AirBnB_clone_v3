#!/usr/bin/python3
"""
Places endpoints
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
def place_by_city_id(city_id):
    """retrieve  place objects from storage by city id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == "POST":
        data = request.get_json(silent=True)
        user_id = data.get("user_id")

        if data is None:
            abort(400, 'Not a JSON')

        if data.get("name") is None:
            abort(400, 'Missing name')

        if user_id is None:
            abort(400, 'Missing user_id')

        if storage.get(User, user_id) is None:
            abort(404)

        new_place = Place(**data)
        new_place.city_id = city_id
        new_place.user_id = user_id
        new_place.save()
        return jsonify(new_place.to_dict()), 201

    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list), 200


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"])
def get_delet_update_places(place_id):
    """retrieve, update or delete a place objects from storage by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        keys = ["id", "user_id", "city_id", "created_at", "updated_at"]

        for key, value in data.items():
            if key not in keys:
                setattr(place, key, value)
        storage.save()

    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"])
def places_search():
    """retrieves all Place objects depending the body of the request."""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    places = storage.all(Place).values()
    states_ids = data.get("states", [])
    cities_ids = data.get("cities", [])
    amenities_id = data.get("amenities", [])

    places_list = [place for place in places]

    if states_ids or cities_ids:
        states = [storage.get(State, state_id) for state_id in states_ids]
        cities_ny_state = [city for state in states for city in state.cities]

        cities = [storage.get(City, city_id) for city_id in cities_ids]

        cities = cities + cities_ny_state
        places_list = [place
                       for city in cities
                       for place in city.places]

    if amenities_id:
        if places_list:
            places = places_list
        places_list = []
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities_id]
        for place in places:
            if all(amenity in place.amenities for amenity in amenities_obj):
                places_list.append(place)

    places = []
    for place in places_list:
        print(place.id)
        place = place.to_dict()
        place.pop('amenities', None)
        places.append(place)
    places_list = places

    return jsonify(places_list), 200

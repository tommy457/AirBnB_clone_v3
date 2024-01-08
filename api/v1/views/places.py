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
    states_ids = data.get("states")
    cities_ids = data.get("cities")
    amenities_id = data.get("amenities")

    if len(data) == 0 or ((states_ids is [] or states_ids is None) and
                          (cities_ids is [] or cities_ids is None) and
                          amenities_id is [] or amenities_id is None):
        places_list = [place.to_dict() for place in places]
        return jsonify(places_list), 200

    if amenities_id is not []:
        amenities_count = storage.count(Amenity)
        places = [place.to_dict()
                  for place in places
                  if len(place.amenities) == amenities_count
                  ]
        return jsonify(places), 200

    if states_ids is not [] or cities_ids is not []:
        states = [storage.get(State, state_id) for state_id in states_ids]
        cities_ny_state = [city for state in states for city in state.cities]

        cities = [storage.get(City, city_id) for city_id in cities_ids]

        cities = cities.extend(cities_ny_state)
        if cities:
            cities = set(cities)
            cities_list = [city.to_dict() for city in cities]

            return jsonify(cities_list), 200
        return jsonify({})

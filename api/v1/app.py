#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
cros = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(err):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """404 handler"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST") or "0.0.0.0",
            port=getenv("HBNB_API_PORT") or "5000",
            threaded=True
            )

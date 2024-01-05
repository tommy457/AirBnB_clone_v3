#!/usr/bin/python3
"""
Index module
"""
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """returns a JSON: status"""
    return {"status": "OK"}

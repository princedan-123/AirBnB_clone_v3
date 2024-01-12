#!/usr/bin/python3
"""A script that creates a route."""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    result = {
                "status": "OK"
            }
    return jsonify(result)

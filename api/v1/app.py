#!/usr/bin/python3
"""An app that returns the status of the API."""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    storage.close()


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", None)
    port = os.environ.get("HBNB_API_PORT", None)
    if host is None or port is None:
        app.run(host="0.0.0.0", port=5000, threaded=True)
    else:
        app.run(host=host, port=port, threaded=True)

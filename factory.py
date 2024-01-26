from flask import Flask
from models import db
from api import api


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)

    return app


def register_extensions(app):
    db.init_app(app)
    api.init_app(app)

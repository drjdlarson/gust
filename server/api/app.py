"""Handles the factory for creating the wsgi application."""
from flask import Flask
from flask_restx import Api

from api.config import env_config

api = Api()


def create_app(config_name):
    #import our resource folder to avoid circular
    #dependency error
    import resources

    app = Flask(__name__)

    app.config.from_object(env_config[config_name])
    api.init_app(app)

    return app

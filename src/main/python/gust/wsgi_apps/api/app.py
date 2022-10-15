"""Handles the factory for creating the wsgi application."""
from flask import Flask
from flask_restx import Api

from gust.wsgi_apps.api.settings import env_config
from gust.wsgi_apps.api.url_bases import BASE

api = Api(prefix="/{:s}".format(BASE))


def create_app(config_name):
    from gust.wsgi_apps.api.resources.drone_namespace import DRONE_NS
    from gust.wsgi_apps.api.resources.zed_namespace import ZED_NS

    app = Flask(__name__)
    app.config.from_object(env_config[config_name])

    api.init_app(app)
    api.add_namespace(ZED_NS)
    api.add_namespace(DRONE_NS)

    return app


if __name__ == "__main__":
    import os
    import gust.wsgi_apps.api.settings as api_app_settings

    from gust.wsgi_apps.setup import initialize_environment

    initialize_environment()
    app = create_app(os.getenv(api_app_settings.ENV_KEY))

    app.run(debug=True)

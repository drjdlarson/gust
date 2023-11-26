"""Handles the factory for creating the wsgi application."""
import logging
from flask import Flask
from flask_restx import Api

import utilities.database as database

# from gust.wsgi_apps.api.settings import env_config
from wsgi_apps.api.url_bases import BASE

api = Api(prefix="/{:s}".format(BASE))


def create_app():
    from wsgi_apps.api.resources.drone_namespace import DRONE_NS

    # from wsgi_apps.api.resources.zed_namespace import ZED_NS

    app = Flask("rest_api")
    # app.config.from_object(env_config[config_name])

    # see https://stackoverflow.com/questions/53548536/how-to-use-the-logging-module-in-python-with-gunicorn
    # see https://stackoverflow.com/questions/53548536/how-to-use-the-logging-module-in-python-with-gunicorn
    # and https://docs.gunicorn.org/en/stable/settings.html#logconfig for a cleaner way with config files that can be passed where we start the process
    # and https://trstringer.com/logging-flask-gunicorn-the-manageable-way/
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    api.init_app(app)
    # api.add_namespace(ZED_NS)
    api.add_namespace(DRONE_NS)

    return app


# if __name__ == "__main__":
#     import os
#     import gust.wsgi_apps.api.settings as api_app_settings

#     from gust.wsgi_apps.setup import initialize_environment

#     initialize_environment()
#     app = create_app(os.getenv(api_app_settings.ENV_KEY))

#     app.run(debug=True)

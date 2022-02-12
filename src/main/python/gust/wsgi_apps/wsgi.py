"""Main entry point for the wsgi app."""
import os

from gust.wsgi_apps.api import app as api_app
import gust.wsgi_apps.api.settings as api_app_settings


rest_api = api_app.create_app(os.getenv(api_app_settings.ENV_KEY))

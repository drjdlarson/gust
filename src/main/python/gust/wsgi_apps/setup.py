import os
import gust.wsgi_apps.api.settings as api_app_settings


def initialize_environment():
    os.environ[api_app_settings.ENV_KEY] = api_app_settings.ENV

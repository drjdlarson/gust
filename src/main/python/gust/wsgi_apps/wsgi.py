"""Main entry point for the wsgi app."""
import os
import platform

from gust.wsgi_apps.api import app as api_app
import gust.wsgi_apps.api.settings as api_app_settings

rest_api = api_app.create_app(os.getenv(api_app_settings.ENV_KEY))

# if 'windows' not in platform.system().lower():
#     from gunicorn.app.base import Application, Config
#     import gunicorn
#     from gunicorn import glogging
#     from gunicorn.workers import sync

#     class GUnicornFlaskApplication(Application):
#         def __init__(self, app):
#             self.usage, self.callable, self.prog, self.app = None, None, None, app

#         def run(self, **options):
#             self.cfg = Config()
#             [self.cfg.set(key, value) for key, value in options.items()]
#             # return self.app.run()
#             return Application.run(self)

#         load = lambda self:self.app

#     rest_api = GUnicornFlaskApplication(api_app.create_app(os.getenv(api_app_settings.ENV_KEY))).app

# else:
    # rest_api = api_app.create_app(os.getenv(api_app_settings.ENV_KEY))

"""Main entry point for the wsgi app."""
import os
from api.app import create_app


app = create_app(os.getenv("LAGER_GUST_ENV"))

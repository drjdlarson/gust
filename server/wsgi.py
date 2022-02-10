"""Main entry point for the wsgi app."""
from api.app import create_app


app = create_app("development")

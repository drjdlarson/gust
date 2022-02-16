from flask_restx import Resource
from gust.wsgi_apps.api.app import api

BASE = '/api'

@api.route('{:s}/<int:a>/<int:b>'.format(BASE))
class SimpleAdder(Resource):
    def get(self, a, b):
        return {'calc': a + b}

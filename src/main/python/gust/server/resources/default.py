from flask_restx import Resource
from gust.server.api.app import api

@api.route('/adder/<int:a>/<int:b>')
class SimpleAdder(Resource):
    def get(self, a, b):
        return {'calc': a + b}

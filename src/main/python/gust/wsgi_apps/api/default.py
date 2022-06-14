from flask_restx import Resource
from gust.wsgi_apps.api.app import api

BASE = '/api'

@api.route('{:s}/addvehicle'.format(BASE))
class Addvehicle(Resource):
    def get(self):
        return {"Newvehicle":22}

@api.route('{:s}/engineOff'.format(BASE))
class engineOff(Resource):
    def get(self):
        return {"Engine Status":0}

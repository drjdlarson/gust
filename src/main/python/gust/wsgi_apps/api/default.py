from flask_restx import Resource
from gust.wsgi_apps.api.app import api

BASE = '/api'

@api.route('{:s}/engine_sw'.format(BASE))
class engine_sw(Resource):
    def get(self):
        return {"Engine Status": 1}

@api.route('{:s}/relay_sw'.format(BASE))
class relay_sw(Resource):
    def get(self):
        return {"Relay Status": 1}

@api.route('{:s}/seluav'.format(BASE))
class seluav(Resource):
    def get(self):
        return {"VehicleName": "SUPER P-1"}

@api.route('{:s}/altitude'.format(BASE))
class altitude(Resource):
    def get(self):
        return {"Altitude": 76}

@api.route('{:s}/vspeed'.format(BASE))
class vspeed(Resource):
    def get(self):
        return {"Vspeed": -2.6}

@api.route('{:s}/airspeed'.format(BASE))
class airspeed(Resource):
    def get(self):
        return {"Airspeed": 6}

@api.route('{:s}/gndspeed'.format(BASE))
class gndspeed(Resource):
    def get(self):
        return {"Gndspeed": 5}

@api.route('{:s}/voltage'.format(BASE))
class voltage(Resource):
    def get(self):
        return {"Voltage": 49.3}

@api.route('{:s}/current'.format(BASE))
class current(Resource):
    def get(self):
        return {"Current": 68}

@api.route('{:s}/mode'.format(BASE))
class mode(Resource):
    def get(self):
        return {"Mode": 2}

@api.route('{:s}/arm'.format(BASE))
class arm(Resource):
    def get(self):
        return {"Arm": 1}

@api.route('{:s}/gnss_fix'.format(BASE))
class gnss_fix(Resource):
    def get(self):
        return {"Gnss_fix": 2}

@api.route('{:s}/roll_angle'.format(BASE))
class roll_angle(Resource):
    def get(self):
        return {"Roll_angle": 20}

@api.route('{:s}/pitch_angle'.format(BASE))
class pitch_angle(Resource):
    def get(self):
        return {"Pitch_angle": -5}

@api.route('{:s}/heading'.format(BASE))
class heading(Resource):
    def get(self):
        return {"Heading": 325}

@api.route('{:s}/next_wp'.format(BASE))
class next_wp(Resource):
    def get(self):
        return {"Next_wp": 3}

@api.route('{:s}/tof'.format(BASE))
class tof(Resource):
    def get(self):
        return {"Tof": 240}

@api.route('{:s}/connection'.format(BASE))
class connection(Resource):
    def get(self):
        return {"Connection": 1}

@api.route('{:s}/track'.format(BASE))
class track(Resource):
    def get(self):
        return {"Track": 330}

@api.route('{:s}/latitude'.format(BASE))
class latitude(Resource):
    def get(self):
        return {"Latitude": 33.912312}

@api.route('{:s}/longitude'.format(BASE))
class longitude(Resource):
    def get(self):
        return {"Longitude": -87.214721}

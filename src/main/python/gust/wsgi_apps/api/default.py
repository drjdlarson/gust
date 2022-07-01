from flask_restx import Resource
from gust.wsgi_apps.api.app import api
import random
from datetime import datetime

now = datetime.now()

BASE = '/api'


@api.route('{:s}/attitude_data'.format(BASE))
class AttitudeData(Resource):
    def get(self):
        return{"id_1": {"roll_angle": 12, "pitch_angle": -4, "altitude": 70, "vspeed": 4, "airspeed": 44, "gndspeed": 46},
               "id_2": {"roll_angle": 15, "pitch_angle": -5, "altitude": 75, "vspeed": 5, "airspeed": 45, "gndspeed": 45}
               }

@api.route('{:s}/sys_status'.format(BASE))
class SysStatus(Resource):
    def get(self):
        return{"id_1": {"name": "SUPER P1", "mode": 0, "arm": 0, "gnss_fix": 2},
               "id_2": {"name": "SUPER P2", "mode": 1, "arm": 1, "gnss_fix": 3}
               }

@api.route('{:s}/sys_data'.format(BASE))
class SysData(Resource):
    def get(self):
        return{"id_1": {"voltage": 50, "current": 30},
               "id_2": {"voltage": 21, "current": 11}
               }

@api.route('{:s}/sys_info'.format(BASE))
class SysInfo(Resource):
    def get(self):
        return{"id_1": {"next_wp": 2, "tof": 240, "relay_sw": 0, "engine_sw": 0, "connection": 0},
               "id_2": {"next_wp": 5, "tof": 333, "relay_sw": 1, "engine_sw": 1, "connection": 1}
               }

@api.route('{:s}/map_data'.format(BASE))
class MapData(Resource):
    def get(self):
        return{"id_1": {"latitude": 33, "longitude": -90, "heading": 240, "track": 250},
               "id_2": {"latitude": -20, "longitude": 95, "heading": 145, "track": 155}
               }

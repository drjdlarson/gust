from flask_restx import Resource
from gust.wsgi_apps.api.app import api
import random
from datetime import datetime

now = datetime.now()

BASE = '/api'




@api.route('{:s}/attitude_data'.format(BASE))
class AttitudeData(Resource):
    def get(self):
        val1 = int(datetime.now().second)
        val2 = int(datetime.now().minute)
        return{1: {"roll_angle": val1 / 2, "pitch_angle": val1 / 3, "altitude": val1, "vspeed": val1 + 20, "airspeed": val1 + 23, "gndspeed": val1 + 15},
               2: {"roll_angle": - val1 / 2, "pitch_angle": -val1 / 3, "altitude": -val1, "vspeed": val1 - 20, "airspeed": val1 + 5, "gndspeed": val1 + 10}
               }

@api.route('{:s}/sys_status'.format(BASE))
class SysStatus(Resource):
    def get(self):
        val1 = random.randint(0, 3)
        val2 = random.randint(0, 2)
        val3 = random.randint(0, 1)
        return{1: {"name": "SUPER P1", "mode": val1, "arm": val3, "gnss_fix": val2},
               2: {"name": "SUPER P2", "mode": val1, "arm": val3, "gnss_fix": val2}
               }

@api.route('{:s}/sys_data'.format(BASE))
class SysData(Resource):
    def get(self):
        val2 = int(datetime.now().minute)
        return{1: {"voltage": val2, "current": val2 + 20},
               2: {"voltage": val2 + 4, "current": val2 + 10}
               }

@api.route('{:s}/sys_info'.format(BASE))
class SysInfo(Resource):
    def get(self):
        val1 = int(datetime.now().second)
        val2 = int(datetime.now().minute)
        val3 = random.randint(0, 30)
        val4 = random.randint(0, 1)
        val5 = random.randint(0, 1)
        return{1: {"next_wp": val3, "tof": 513 + val1, "relay_sw": val4, "engine_sw": val5, "connection": 1},
               2: {"next_wp": val2 + 1, "tof": 451 + val1, "relay_sw": val5, "engine_sw": val4, "connection": 1}
               }

@api.route('{:s}/map_data'.format(BASE))
class MapData(Resource):
    def get(self):
        val1 = int(datetime.now().second)
        return{1: {"latitude": 33.121560, "longitude": -81.421345, "heading": 240 + 8 * val1, "track": 250 + 4 * val1},
               2: {"latitude": 33.250450, "longitude": -81.421321, "heading": 145 + 5 * val1, "track": 155 + 4 * val1}
               }

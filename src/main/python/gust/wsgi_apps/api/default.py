from flask_restx import Resource
from gust.wsgi_apps.api.app import api
import random
from datetime import datetime

import logging
import gust.database_test as database

now = datetime.now()

BASE = '/api'


@api.route('{:s}/attitude_data'.format(BASE))
class AttitudeData(Resource):
    params = ['roll_angle', 'pitch_angle', 'altitude', 'vspeed', 'airspeed', 'gndspeed']

    def get(self):
        attitude_data = {}
        database.open()
        names = database.get_drone_ids(True)
        for index, drone in enumerate(names):
            table_name = database.create_drone_rate_table_name(drone, database.DroneRates.RATE2)
            key = index + 1
            attitude_data[key] = database.get_params(table_name, AttitudeData.params)
        return attitude_data


@api.route('{:s}/sys_status'.format(BASE))
class SysStatus(Resource):
    params = ['flt_mode', 'arm', 'gnss_fix']

    def get(self):
        sys_status = {}
        database.open()
        names = database.get_drone_ids(True)
        for index, drone in enumerate(names):
            table_name = database.create_drone_rate_table_name(drone, database.DroneRates.RATE1)
            key = index + 1
            sys_status[key] = database.get_params(table_name, SysStatus.params)
            name_dict = {"name": drone}
            sys_status[key].update(name_dict)
        return sys_status


@api.route('{:s}/sys_data'.format(BASE))
class SysData(Resource):
    params = ['voltage', 'current']

    def get(self):
        sys_data = {}
        database.open_db()
        names = database.get_drone_ids(True)
        for index, drone in enumerate(names):
            table_name = database.create_drone_rate_table_name(drone, database.DroneRates.RATE1)
            key = index + 1
            sys_data[key] = database.get_params(table_name, SysData.params)
        return sys_data


@api.route('{:s}/sys_info'.format(BASE))
class SysInfo(Resource):
    params = ['next_wp', 'tof', 'relay_sw', 'engine_sw', 'connection']

    def get(self):
        sys_info = {}
        database.open_db()
        names = database.get_drone_ids(True)
        for index, drone in enumerate(names):
            table_name = database.create_drone_rate_table_name(drone, database.DroneRates.RATE1)
            key = index + 1
            sys_info[key] = database.get_params(table_name, SysInfo.params)
        return sys_info


@api.route('{:s}/map_data'.format(BASE))
class MapData(Resource):
    params = ['latitude', 'longitude', 'heading', 'track']

    def get(self):
        map_data = {}
        database.open_db()
        names = database.get_drone_ids(True)
        for index, drone in enumerate(names):
            table_name = database.create_drone_rate_table_name(drone, database.DroneRates.RATE2)
            key = index + 1
            map_data[key] = database.get_params(table_name, MapData.params)
        return map_data

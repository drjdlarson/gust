from flask_restx import Resource
from gust.wsgi_apps.api.app import api
import random
from datetime import datetime
from flask import request
import serial.tools.list_ports


import logging
import gust.database as database
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot

now = datetime.now()

BASE = '/api'
logger = logging.getLogger('[URL-Manager]')


class Communicator(QObject):

    signal = pyqtSignal(dict)
    sig_value = {}

    def __init__(self):
        super().__init__()

    def send_signal(self):
        self.signal.connect(self.handle_trigger)
        self.signal.emit(self.sig_value)
        return self.result

    @pyqtSlot(dict)
    def handle_trigger(self, passed_signal):
        logger.critical("we are in the handle_trigger function")
        # logger.critical("name is {} and port is {}".format(passed_signal['name'], passed_signal['port']))
        self.result = True



@api.route('{:s}/connect_drone'.format(BASE))
class ConnInfo(Resource):
    def get(self):
        port = request.args.get('port', default='', type=str)
        name = request.args.get('name', default='', type=str)

        if len(port) > 0 and len(name) > 0:
            sig = {'name': name, 'port': port}
            Communicator.sig_value = sig
            success = Communicator().send_signal()

            if success:
                logger.critical("it works")
                return {'success': success, 'msg': ''}
            elif not success:
                return {'success': False, 'msg': "Error Connecting"}

        elif len(port) == 0:
            return {'success': False, 'msg': 'Invalid port'}

        elif len(name) == 0:
            return {'success': False, 'msg': 'Invalid name'}


@api.route('{:s}/get_available_ports'.format(BASE))
class PortsData(Resource):
    def get(self):
        ports = list(serial.tools.list_ports.comports())
        available_ports = ['/dev/test']
        for port in sorted(ports):
            available_ports.append(port.device)
        return {'ports': available_ports}


@api.route('{:s}/attitude_data'.format(BASE))
class AttitudeData(Resource):
    params = ['roll_angle', 'pitch_angle', 'altitude', 'vspeed', 'airspeed', 'gndspeed']

    def get(self):
        attitude_data = {}
        database.open_db()
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
        database.open_db()
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

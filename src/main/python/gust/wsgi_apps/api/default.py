from flask_restx import Resource
from gust.wsgi_apps.api.app import api
import random
from datetime import datetime
from flask import request
import serial.tools.list_ports


import logging
import gust.database as database
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot, QObject
import gust.conn_manager.conn_settings as conn_settings
import socket
import json

BASE = "/api"
logger = logging.getLogger("[URL-Manager]")


def send_info_to_conn_server(info_dict, msg_type):
    """
    Packages and sends information to conn_server as a UDP socket client

    Parameters
    ----------
    info_dict : dict
        Information to be sent to conn_server
    msg_type : str
        Type of information in the dictionary.
        msg_type can be specified based on conn_settings

    Returns
    -------
    bool
        Success result.
    str
        Any extra message.

    """


    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(conn_settings.TIMEOUT)

    msg = {'type': msg_type}
    msg.update(info_dict)

    f_msg = json.dumps(msg).encode(conn_settings.FORMAT)
    client.sendto(f_msg, conn_settings.ADDR())

    # Try to receive data being sent back from conn_server
    try:
        response, addr = client.recvfrom(conn_settings.MAX_MSG_SIZE)
        msg = json.loads(response.decode(conn_settings.FORMAT))
        return msg['success'], msg['info']

    except socket.timeout:
        return False, msg['info']



@api.route("{:s}/connect_drone".format(BASE))
class ConnInfo(Resource):
    def get(self):
        port = request.args.get("port", default="", type=str)
        name = request.args.get("name", default="", type=str)
        vehicle_info = {'name': name, 'port': port}

        if len(port) > 0 and len(name) > 0:
            success, info = send_info_to_conn_server(vehicle_info, conn_settings.DRONE_CONN)

            if success:
                return {"success": True, "msg": ""}
            elif not success:
                return {"success": False, "msg": "error connecting"}

        elif len(port) == 0:
            return {"success": False, "msg": "Invalid port"}
        elif len(name) == 0:
            return {"success": False, "msg": "Invalid name"}



@api.route("{:s}/get_available_ports".format(BASE))
class PortsData(Resource):
    def get(self):
        ports = list(serial.tools.list_ports.comports())
        available_ports = ["/dev/test"]
        for port in sorted(ports):
            available_ports.append(port.device)
        return {"ports": available_ports}


@api.route("{:s}/attitude_data".format(BASE))
class AttitudeData(Resource):
    params = ["roll_angle", "pitch_angle", "altitude", "vspeed", "airspeed", "gndspeed"]

    def get(self):
        attitude_data = {}
        database.open_db()
        names = database.get_drone_ids(True)
        for index, drone in enumerate(names):
            table_name = database.create_drone_rate_table_name(
                drone, database.DroneRates.RATE2
            )
            key = index + 1
            attitude_data[key] = database.get_params(table_name, AttitudeData.params)
        return attitude_data


@api.route("{:s}/sys_status".format(BASE))
class SysStatus(Resource):
    params = ["flt_mode", "arm", "gnss_fix"]

    def get(self):
        sys_status = {}
        database.open_db()
        names = database.get_drone_ids(True)
        for index, drone in enumerate(names):
            table_name = database.create_drone_rate_table_name(
                drone, database.DroneRates.RATE1
            )
            key = index + 1
            sys_status[key] = database.get_params(table_name, SysStatus.params)
            name_dict = {"name": drone}
            sys_status[key].update(name_dict)
        return sys_status


@api.route("{:s}/sys_data".format(BASE))
class SysData(Resource):
    params = ["voltage", "current"]

    def get(self):
        sys_data = {}
        database.open_db()
        names = database.get_drone_ids(True)
        for index, drone in enumerate(names):
            table_name = database.create_drone_rate_table_name(
                drone, database.DroneRates.RATE1
            )
            key = index + 1
            sys_data[key] = database.get_params(table_name, SysData.params)
        return sys_data


@api.route("{:s}/sys_info".format(BASE))
class SysInfo(Resource):
    params = ["next_wp", "tof", "relay_sw", "engine_sw", "connection"]

    def get(self):
        sys_info = {}
        database.open_db()
        names = database.get_drone_ids(True)
        for index, drone in enumerate(names):
            table_name = database.create_drone_rate_table_name(
                drone, database.DroneRates.RATE1
            )
            key = index + 1
            sys_info[key] = database.get_params(table_name, SysInfo.params)
        return sys_info


@api.route("{:s}/map_data".format(BASE))
class MapData(Resource):
    params = ["latitude", "longitude", "heading", "track"]

    def get(self):
        map_data = {}
        database.open_db()
        names = database.get_drone_ids(True)
        for index, drone in enumerate(names):
            table_name = database.create_drone_rate_table_name(
                drone, database.DroneRates.RATE2
            )
            key = index + 1
            map_data[key] = database.get_params(table_name, MapData.params)
        return map_data

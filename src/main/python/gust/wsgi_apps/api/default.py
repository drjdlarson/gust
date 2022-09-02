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

    msg = {"type": msg_type}
    msg.update(info_dict)

    f_msg = json.dumps(msg).encode(conn_settings.FORMAT)
    client.sendto(f_msg, conn_settings.ADDR())

    # Try to receive data being sent back from conn_server
    try:
        response, addr = client.recvfrom(conn_settings.MAX_MSG_SIZE)
        msg = json.loads(response.decode(conn_settings.FORMAT))
        return msg["success"], msg["info"]

    except socket.timeout:
        msg = "Timeout on connection with backend"
        return False, msg["info"]


@api.route("{:s}/connect_drone".format(BASE))
class ConnInfo(Resource):
    def get(self):
        port = request.args.get("port", default="", type=str)
        name = request.args.get("name", default="", type=str)
        vehicle_info = {"name": name, "port": port}

        if len(port) > 0 and len(name) > 0:
            database.connect_db()
            res = database.add_vehicle(name, port)
            if res:
                conn_succ, info = send_info_to_conn_server(
                    vehicle_info, conn_settings.DRONE_CONN
                    )
                if conn_succ:
                    return {"success": True, "msg": ""}
                elif not conn_succ:
                    return {"success": False, "msg": "Error connecting"}
            else:
                return {'success': False, 'msg': "Unable to add vehicle to database"}
        elif len(port) == 0:
            return {"success": False, "msg": "Invalid port"}
        elif len(name) == 0:
            return {"success": False, "msg": "Invalid name"}


@api.route("{:s}/disconnect_drone".format(BASE))
class Disconnect(Resource):
    def get(self):
        name = request.args.get("name", default="", type=str)
        disconn_succ, info = send_info_to_conn_server({'name': name}, conn_settings.DRONE_DISC)
        if disconn_succ:
            return {"success": True, 'msg': ""}
        else:
            return {"success": False, "msg": "Unable to disconnect"}


@api.route("{:s}/get_available_ports".format(BASE))
class PortsData(Resource):
    def get(self):
        ports = list(serial.tools.list_ports.comports())
        available_ports = ["/dev/test/"]
        for port in sorted(ports):
            available_ports.append(port.device)
        return {"ports": available_ports}

@api.route("{:s}/sys_data".format(BASE))
class SysData(Resource):
    params = ["home_lat", "home_lon", "home_alt", "voltage", "current"]

    def get(self):
        sys_data = {}
        database.connect_db()
        names = database.get_drone_ids()
        for index, name in enumerate(names):
            table_name = database.create_drone_rate_table_name(
                name, database.DroneRates.RATE1
            )
            key = index + 1
            sys_data[key] = database.get_params(table_name, SysData.params)
        return sys_data


@api.route("{:s}/attitude_data".format(BASE))
class AttitudeData(Resource):
    params = ["roll_angle", "pitch_angle", "alpha", "beta", "airspeed", "gndspeed", "vspeed", "throttle"]

    def get(self):
        attitude_data = {}
        database.connect_db()
        names = database.get_drone_ids()
        for index, name in enumerate(names):
            table_name = database.create_drone_rate_table_name(
                name, database.DroneRates.RATE2
            )
            key = index + 1
            attitude_data[key] = database.get_params(table_name, AttitudeData.params)
        return attitude_data


@api.route("{:s}/pos_data".format(BASE))
class PosData(Resource):
    params = ["latitude", "longitude", "relative_alt", "heading", "track", "gnss_fix", "satellites_visible"]

    def get(self):
        pos_data = {}
        database.connect_db()
        names = database.get_drone_ids()
        for index, name in enumerate(names):
            table_name = database.create_drone_rate_table_name(
                name, database.DroneRates.RATE2
            )
            key = index + 1
            pos_data[key] = database.get_params(table_name, PosData.params)
            pos_data[key].update({'name': name})
        return pos_data


@api.route("{:s}/sys_info".format(BASE))
class SysInfo(Resource):
    params = ["armed", "flight_mode", "mav_type", "autopilot", "custom_mode", "tof", "next_wp", "relay_sw", "engine_sw", "connection"]

    def get(self):
        sys_info = {}
        database.connect_db()
        names = database.get_drone_ids()
        for index, name in enumerate(names):
            table_name = database.create_drone_rate_table_name(
                name, database.DroneRates.RATE4
            )
            key = index + 1
            sys_info[key] = database.get_params(table_name, SysInfo.params)
        return sys_info


@api.route("{:s}/channels_info".format(BASE))
class ChannelsData(Resource):
    params = ["chancount", "chan1_raw", "chan2_raw", "chan3_raw", "chan4_raw",
              "chan5_raw", "chan6_raw", "chan7_raw", "chan8_raw", "chan9_raw",
              "chan10_raw", "chan11_raw", "chan12_raw", "chan13_raw",
              "chan14_raw", "chan15_raw", "chan16_raw", "chan17_raw", "chan18_raw",
              "rssi", "servo_port", "servo1_raw", "servo2_raw", "servo3_raw",
              "servo4_raw", "servo5_raw", "servo6_raw", "servo7_raw", "servo8_raw",
              "servo9_raw", "servo10_raw", "servo11_raw", "servo12_raw",
              "servo13_raw", "servo14_raw", "servo15_raw", "servo16_raw"]

    def get(self):
        channels_info = {}
        database.connect_db()
        names = database.get_drone_ids()
        for index, name in enumerate(names):
            table_name = database.create_drone_rate_table_name(
                name, database.DroneRates.RATE3
            )
            key = index + 1
            channels_info[key] = database.get_params(table_name, ChannelsData.params)
        return channels_info

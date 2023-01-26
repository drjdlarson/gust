"""Defines main urls for wsgi app."""
import serial.tools.list_ports
import logging
from flask_restx import Resource, Namespace
from flask import request

import utilities.database as database
from utilities import ConnSettings as conn_settings
from wsgi_apps.api.url_bases import DRONE
from utilities import send_info_to_udp_server


logger = logging.getLogger("[URL-Manager]")

DRONE_NS = Namespace(DRONE)
conParse = DRONE_NS.parser()
conParse.add_argument("port", default="", type=str)
conParse.add_argument("name", default="", type=str)
conParse.add_argument("color", default="", type=str)
conParse.add_argument("baud", default=-1, type=int)

uploadParse = DRONE_NS.parser()
uploadParse.add_argument("name", default="", type=str)
uploadParse.add_argument("wp_color", default="", type=str)

cmdParse = DRONE_NS.parser()
cmdParse.add_argument("name", default="", type=str)
cmdParse.add_argument("cmd", default="", type=str)
cmdParse.add_argument("param", default="", type=str)


@DRONE_NS.route("/connect")
class ConnInfo(Resource):
    @DRONE_NS.expect(conParse)
    def get(self):
        args = conParse.parse_args()
        port = args["port"]
        name = args["name"]
        color = args["color"]
        baud = args["baud"]

        vehicle_info = {"name": name, "port": port, "color": color, "baud": baud}

        if len(port) > 0 and len(name) > 0:
            if not database.connect_db():
                return {"success": False, "msg": "Failed to connect to database"}

            res = database.add_vehicle(name, port, color)
            if res:
                conn_succ, info = send_info_to_udp_server(
                    vehicle_info, conn_settings.DRONE_CONN
                )
                if conn_succ:
                    return {"success": True, "msg": ""}
                elif not conn_succ:
                    return {"success": False, "msg": info}
            else:
                return {"success": False, "msg": "Unable to add vehicle to database"}
        elif len(port) == 0:
            return {"success": False, "msg": "Invalid port"}
        elif len(name) == 0:
            return {"success": False, "msg": "Invalid name"}


@DRONE_NS.route("/autopilot_cmd")
class AutopilotCmd(Resource):
    @DRONE_NS.expect(cmdParse)
    def get(self):
        args = cmdParse.parse_args()
        name = args["name"]
        cmd = args["cmd"]
        param = args["param"]

        cmd_info = {"name": name, "cmd": cmd, "param": param}
        logger.info(cmd_info)

        cmd_succ, info = send_info_to_udp_server(cmd_info, conn_settings.AUTO_CMD)
        if cmd_succ:
            return {"success": True, "msg": ""}
        else:
            return {"success": False, "msg": info}


@DRONE_NS.route("/upload_wp")
class UploadWP(Resource):
    cmr_started = False

    @DRONE_NS.expect(uploadParse)
    def get(self):
        args = uploadParse.parse_args()
        name = args["name"]
        wp_color = args["wp_color"]

        upload_info = {"name": name, "wp_color": wp_color}

        if not database.connect_db():
            return {"success": False, "msg": "Failed to connect to database"}

        if not self.cmr_started:
            res = database.add_cmr_table()

        res = database.add_cmr_vehicle(name, wp_color)
        if res:
            self.cmr_started = True
            upload_succ, info = send_info_to_udp_server(
                upload_info, conn_settings.UPLOAD_WP
            )
            if upload_succ:
                return {"success": True, "msg": ""}
            elif not upload_succ:
                return {"success": False, "msg": info}
        else:
            return {
                "success": False,
                "msg": "Unable to add waypoint info to the database",
            }


@DRONE_NS.route("/disconnect")
class Disconnect(Resource):
    def get(self):
        name = request.args.get("name", default="", type=str)
        disconn_succ, info = send_info_to_udp_server(
            {"name": name}, conn_settings.DRONE_DISC
        )
        if disconn_succ:
            return {"success": True, "msg": ""}
        else:
            return {"success": False, "msg": "Unable to disconnect"}


@DRONE_NS.route("/start_cmr_proc")
class CmrProcessTrigger(Resource):
    def get(self):
        succ, info = send_info_to_udp_server({}, conn_settings.START_CMR)
        return {"success": succ, "msg": info}


@DRONE_NS.route("/stop_cmr_proc")
class CmrProcessStop(Resource):
    def get(self):
        succ, info = send_info_to_udp_server({}, conn_settings.STOP_CMR)
        return {"success": succ, "msg": info}


@DRONE_NS.route("/get_connected_drones_with_color")
class DroneAndColor(Resource):
    def get(self):
        drone_and_colors = {}
        database.connect_db()
        names = database.get_drone_ids()
        for name in names:
            color = database.get_drone_color(name)
            drone_and_colors[name] = color
        return drone_and_colors


@DRONE_NS.route("/get_available_ports")
class PortsData(Resource):
    def get(self):
        ports = list(serial.tools.list_ports.comports())
        available_ports = ["/dev/test/"]
        for port in sorted(ports):
            available_ports.append(port.device)
        return {"ports": available_ports}


@DRONE_NS.route("/get_used_colors")
class ColorsData(Resource):
    def get(self):
        database.connect_db()
        used_colors = database.get_used_colors()
        return {"used_colors": used_colors}

@DRONE_NS.route("/start_sil")
class StartSIL(Resource):
    def get(self):
        start_sil = {}
        sil_succ, info = send_info_to_udp_server(start_sil, conn_settings.START_SIL)
        if sil_succ:
            return {"success": True, "msg": ""}
        else:
            return {"success": False, "msg": info}

@DRONE_NS.route("/sys_data")
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


@DRONE_NS.route("/attitude_data")
class AttitudeData(Resource):
    params = [
        "roll_angle",
        "pitch_angle",
        "alpha",
        "beta",
        "airspeed",
        "gndspeed",
        "vspeed",
        "throttle",
    ]

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


@DRONE_NS.route("/pos_data")
class PosData(Resource):
    params = [
        "latitude",
        "longitude",
        "relative_alt",
        "yaw",
        "heading",
        "gnss_fix",
        "satellites_visible",
    ]

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
            pos_data[key].update({"name": name})
        return pos_data


@DRONE_NS.route("/sys_info")
class SysInfo(Resource):
    params = [
        "armed",
        "flight_mode",
        "mav_type",
        "autopilot",
        "custom_mode",
        "tof",
        "next_wp",
        "relay_sw",
        "engine_sw",
    ]

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
            sys_info[key].update({"color": database.get_drone_color(name)})
        return sys_info


@DRONE_NS.route("/channels_info")
class ChannelsData(Resource):
    params = [
        "chancount",
        "chan1_raw",
        "chan2_raw",
        "chan3_raw",
        "chan4_raw",
        "chan5_raw",
        "chan6_raw",
        "chan7_raw",
        "chan8_raw",
        "chan9_raw",
        "chan10_raw",
        "chan11_raw",
        "chan12_raw",
        "chan13_raw",
        "chan14_raw",
        "chan15_raw",
        "chan16_raw",
        "chan17_raw",
        "chan18_raw",
        "rssi",
        "servo_port",
        "servo1_raw",
        "servo2_raw",
        "servo3_raw",
        "servo4_raw",
        "servo5_raw",
        "servo6_raw",
        "servo7_raw",
        "servo8_raw",
        "servo9_raw",
        "servo10_raw",
        "servo11_raw",
        "servo12_raw",
        "servo13_raw",
        "servo14_raw",
        "servo15_raw",
        "servo16_raw",
    ]

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

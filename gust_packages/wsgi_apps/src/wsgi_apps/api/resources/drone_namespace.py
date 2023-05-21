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

# Receives arguments for vehicle connection
conParse = DRONE_NS.parser()
conParse.add_argument("port", default="", type=str)
conParse.add_argument("name", default="", type=str)
conParse.add_argument("color", default="", type=str)
conParse.add_argument("baud", default=-1, type=int)

# Receives arguments for mission upload
uploadParse = DRONE_NS.parser()
uploadParse.add_argument("name", default="", type=str)
uploadParse.add_argument("filename", default="", type=str)
uploadParse.add_argument("mission_type", default="", type=str)
uploadParse.add_argument("wp_color", default="", type=str)

# Receives arguments for Autopilot commands
cmdParse = DRONE_NS.parser()
cmdParse.add_argument("name", default="", type=str)
cmdParse.add_argument("cmd", default="", type=str)
cmdParse.add_argument("param", default="", type=str)

# Receives arguments for starting SIL
silParse = DRONE_NS.parser()
silParse.add_argument("sil_name", default="", type=str)
silParse.add_argument("vehicle_type", default="", type=str)
silParse.add_argument("home", default="", type=str)


@DRONE_NS.route("/connect")
class ConnInfo(Resource):
    """Handles initial connection to the vehicle"""

    @DRONE_NS.expect(conParse)
    def get(self):
        args = conParse.parse_args()
        port = args["port"]
        name = args["name"]
        color = args["color"]
        baud = args["baud"]

        vehicle_info = {
            "name": name,
            "port": port,
            "color": color,
            "baud": baud,
        }
        logger.info(vehicle_info)

        # Connect to database
        if len(port) > 0 and len(name) > 0:
            if not database.connect_db():
                return {
                    "success": False,
                    "msg": "Failed to connect to database",
                }

            # Add vehicle info in the database
            res = database.add_vehicle(name, port, color)

            # Send message to ConnServer to connect to the vehicle
            # send_info_to_udp_server() is used to package the message nicely for the
            # UDP socket server in ConnServer.
            if res:
                conn_succ, info = send_info_to_udp_server(
                    vehicle_info, conn_settings.DRONE_CONN
                )
                if conn_succ:
                    return {"success": True, "msg": ""}
                # Receiving error message from ConnServer.
                elif not conn_succ:
                    return {"success": False, "msg": info}

            else:
                return {
                    "success": False,
                    "msg": "Unable to add vehicle to database",
                }

        elif len(port) == 0:
            return {"success": False, "msg": "Invalid port"}
        elif len(name) == 0:
            return {"success": False, "msg": "Invalid name"}


@DRONE_NS.route("/autopilot_cmd")
class AutopilotCmd(Resource):
    """Handles relay of autopilot command to the vehicle"""

    @DRONE_NS.expect(cmdParse)
    def get(self):
        args = cmdParse.parse_args()
        name = args["name"]
        cmd = args["cmd"]
        param = args["param"]

        # package as a dict
        cmd_info = {"name": name, "cmd": cmd, "param": param}
        logger.info(cmd_info)

        cmd_succ, info = send_info_to_udp_server(cmd_info, conn_settings.AUTO_CMD)

        if cmd_succ:
            return {"success": True, "msg": ""}
        else:
            return {"success": False, "msg": info}


@DRONE_NS.route("/download_wp")
class DownloadWP(Resource):
    """Handles downloading of waypoint."""

    def get(self):
        # to send any specific command to the radio. Currently, no messages are needed.
        download_info = {}

        # Save all downloaded mission items here.
        all_waypoints = {}

        # Connect to database
        if not database.connect_db():
            return {
                "success": False,
                "msg": "Failed to connect to database",
            }

        # This tells the ConnServer to download mission items from the vehicle.
        # The downloaded mission items are then saved to the database by RadioManager.
        download_succ, info = send_info_to_udp_server(
            download_info, conn_settings.DOWNLOAD_WP
        )

        if download_succ:
            database.connect_db()
            names = database.get_drone_ids()

            # Downloading for all connected vehicles.
            for name in names:
                wp_list = database.get_mission_items(name)
                all_waypoints[name] = [s for s in wp_list if s != (0.0, 0.0)]
            return all_waypoints

        else:
            return {"success": False, "msg": "Unable to get latest waypoints."}



@DRONE_NS.route("/upload_wp")
class UploadWP(Resource):
    """Handles Mission upload to the vehicle"""

    cmr_started = False

    @DRONE_NS.expect(uploadParse)
    def get(self):
        args = uploadParse.parse_args()
        name = args["name"]
        filename = args["filename"]
        mission_type = args["mission_type"]

        # optional (used for missions like CMR)
        wp_color = args["wp_color"]

        upload_info = {"name": name, "filename": filename}
        logger.info(upload_info)

        if mission_type == conn_settings.CMR:
            if not self.cmr_started:
                # only required for the first CMR mission upload
                res = database.add_cmr_table()
            res = database.add_cmr_vehicle(name, wp_color)
            if res:
                self.cmr_started = True
                return self.send_upload_msg(upload_info)
            else:
                return {
                    "success": False,
                    "msg": "Unable to add waypoint info to the database",
                }

        # put other mission types here
        # elif mission_type ==
            ##############

        else:
            return {"success": False, "msg": "Invalid Mission Type"}

    def send_upload_msg(self, upload_info):
        """
        Send message to ConnServer to upload mission.

        Parameters
        ----------
        upload_info: dict
            Information including vehicle name and mission file's path

        Returns
        -------
        {'success': bool, "msg": str}
        """
        upload_succ, info = send_info_to_udp_server(
            upload_info, conn_settings.UPLOAD_WP
        )
        if upload_succ:
            return {"success": True, "msg": ""}
        elif not upload_succ:
            return {"success": False, "msg": info}


@DRONE_NS.route("/disconnect")
class Disconnect(Resource):
    """Handles disconnection of vehicle"""

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
    """Handles Start of CMR QProcess"""

    def get(self):
        succ, info = send_info_to_udp_server({}, conn_settings.START_CMR)
        return {"success": succ, "msg": info}


@DRONE_NS.route("/stop_cmr_proc")
class CmrProcessStop(Resource):
    """Handles termination of CMR QProcess"""

    def get(self):
        succ, info = send_info_to_udp_server({}, conn_settings.STOP_CMR)
        return {"success": succ, "msg": info}


@DRONE_NS.route("/get_connected_drones_with_color")
class DroneAndColor(Resource):
    """Finds color information for each vehicle"""

    def get(self):
        """Returns a dict with {vehicle_name: color}"""

        # The color information for the vehicle is stored in database.
        drone_and_colors = {}
        database.connect_db()
        names = database.get_drone_ids()
        for name in names:
            color = database.get_drone_color(name)
            drone_and_colors[name] = color
        return drone_and_colors


@DRONE_NS.route("/get_saved_locations")
class SavedLocations(Resource):
    """Finds all the saved locations information"""

    def get(self):
        """Returns a dict with {location_name: (lat, lon)}"""

        # This information is stored in the database at startup.
        database.connect_db()
        saved_locations = database.get_saved_locations()
        for name, coords in saved_locations.items():
            saved_locations[name] = tuple(saved_locations[name].split(","))
        return saved_locations


@DRONE_NS.route("/get_available_ports")
class PortsData(Resource):
    """Finds all the ports in the host hardware."""

    def get(self):
        ports = list(serial.tools.list_ports.comports())
        available_ports = []
        for port in sorted(ports):
            available_ports.append(port.device)
        return {"ports": available_ports}


@DRONE_NS.route("/get_used_colors")
class ColorsData(Resource):
    """Finds all the colors that are already used (From database)"""

    def get(self):
        database.connect_db()
        used_colors = database.get_used_colors()
        return {"used_colors": used_colors}


@DRONE_NS.route("/start_sil")
class StartSIL(Resource):
    """Handles start of Ardupilot SIL."""

    @DRONE_NS.expect(silParse)
    def get(self):
        args = silParse.parse_args()
        start_sil = {
            "sil_name": args["sil_name"],
            "vehicle_type": args["vehicle_type"],
            "home": args["home"],
        }

        sil_succ, info = send_info_to_udp_server(start_sil, conn_settings.START_SIL)

        if sil_succ:
            return {"success": True, "msg": ""}
        else:
            return {"success": False, "msg": info}


@DRONE_NS.route("/sys_data")
class SysData(Resource):
    """Handles retrieving System Data from the database"""

    # This class picks only the following data.
    params = ["home_lat", "home_lon", "home_alt", "voltage", "current"]

    def get(self):
        sys_data = {}
        database.connect_db()
        names = database.get_drone_ids()

        # For all vehicles in the database, grab the data listed in params.
        for index, name in enumerate(names):

            # The tables in the database are named a certain way.
            # See utilities.database for more.
            table_name = database.create_drone_rate_table_name(
                name, database.DroneRates.RATE1
            )
            key = index + 1

            # Requesting SysData.params data from table_name.
            # The tables in database store data under same name as in params.
            # So DO NOT change the strings in SysData.params.
            sys_data[key] = database.get_params(table_name, SysData.params)
        return sys_data


@DRONE_NS.route("/attitude_data")
class AttitudeData(Resource):
    """Handles retrieving Attitude data from the database"""

    # Similar to SysData (see above).

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
    """Handles retrieving Position data from the database"""

    # Similar to SysData (see above).

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
    """Handles retrieving more system and mission data from the database"""

    # Similar to SysData (see above).

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
    """Handles retrieving RC and servo channels data from the database"""

    # Similar to SysData (see above).

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

"""GUST plugin for Radio Manager."""
import argparse, math
import dronekit
import random
import time
import numpy as np
import logging
import sys
import signal
import os
import json
from PyQt5 import QtNetwork
import utilities.database as database
from utilities import ConnSettings as conn_settings
from argparse import ArgumentParser
from radio_manager import logger

d2r = np.pi / 100
r2d = 1 / d2r


# %% Custom Functions


def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two `LocationGlobal` or `LocationGlobalRelative` objects.

    Based on Haversine equations
    """
    del_lat = aLocation2.lat - aLocation1.lat
    del_lon = aLocation2.lon - aLocation1.lon
    a = (math.sin(del_lat / 2)) ** 2 + math.cos(aLocation1.lat) * math.cos(
        aLocation2.lat
    ) * (math.sin(del_lon / 2)) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = 6378100 * c
    return d


def distance_to_current_waypoint(radio):
    """
    Gets distance in metres to the current waypoint.
    It returns None for the first waypoint (Home location).
    """
    nextwaypoint = radio.commands.next
    if nextwaypoint == 0:
        return None
    missionitem = radio.commands[nextwaypoint - 1]  # commands are zero indexed
    lat = missionitem.x
    lon = missionitem.y
    alt = missionitem.z
    targetWaypointLocation = dronekit.LocationGlobalRelative(lat, lon, alt)
    distancetopoint = get_distance_metres(
        radio.location.global_frame, targetWaypointLocation
    )
    return distancetopoint


def goto_next_wp(received_signal, radio):
    radio.commands.next = radio.commands.next + 1
    succ = True
    err = "Going to wp: {}".format(radio.commands.next)
    return succ, err


def set_mode(mode, radio):
    if radio is None:
        succ = False
        err = "Not Connected to radio"
    else:
        radio.mode = dronekit.VehicleMode(mode)
        succ = True
        err = ""
    return succ, err


def take_off(take_off_alt, radio):
    if radio is None:
        succ = False
        err = "Not Connected to radio"
    else:
        logger.info("Basic pre-arm checks")
        while not radio.is_armable:
            logger.info("waiting for vehicle to initialize")
            time.sleep(1)

        logger.info("arming motors")
        radio.mode = dronekit.VehicleMode("GUIDED")
        radio.armed = True

        while not radio.armed:
            logger.info("waiting for arming...")
            time.sleep(1)

        logger.info("Taking off...")
        radio.simple_takeoff(take_off_alt)
        succ = True
        err = ""
    return succ, err


def arm_disarm(bool_val, radio):
    if radio.armed is not bool_val:
        radio.armed = bool_val
        succ = True
        err = " "
    else:
        succ = False
        err = "Armed state is already {}".format(bool_val)


def upload_waypoints(received_signal, radio):
    """Upload a mission from a file"""
    filename = received_signal["filename"]

    missionList = readmission(filename, radio)
    logger.info("Uploading waypoints from {}\n".format(filename))
    logger.info("Clearing older mission\n")

    cmds = radio.commands
    cmds.clear()
    cmds.upload()

    logger.info("uploading new mission\n")
    for command in missionList:
        cmds.add(command)
    logger.info("Added all commands")
    cmds.upload(timeout=20)
    logger.info("Uploaded the mission")

    succ = True
    err = ""
    return succ, err


def readmission(filename, radio):
    """
    Load a mission from a file into a list.

    This function is used by upload_mission().
    """
    print("Reading mission from file: {}\n".format(filename))
    cmds = radio.commands
    missionlist = []
    with open(filename) as f:
        for i, line in enumerate(f):
            if i == 0:
                if not line.startswith("QGC WPL 110"):
                    raise Exception("File is not supported WP version")
            else:
                linearray = line.split("\t")
                ln_seq = int(linearray[0])
                ln_currentwp = int(linearray[1])
                ln_frame = int(linearray[2])
                ln_command = int(linearray[3])
                ln_param1 = float(linearray[4])
                ln_param2 = float(linearray[5])
                ln_param3 = float(linearray[6])
                ln_param4 = float(linearray[7])
                ln_x = float(linearray[8])
                ln_y = float(linearray[9])
                ln_z = float(linearray[10])
                ln_autocontinue = int(linearray[11])
                cmd = dronekit.Command(
                    0,
                    0,
                    0,
                    ln_frame,
                    ln_command,
                    0,
                    0,
                    ln_param1,
                    ln_param2,
                    ln_param3,
                    ln_param4,
                    ln_x,
                    ln_y,
                    ln_z,
                )
                logger.info(
                    "\n{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                        0,
                        0,
                        0,
                        ln_frame,
                        ln_command,
                        0,
                        0,
                        ln_param1,
                        ln_param2,
                        ln_param3,
                        ln_param4,
                        ln_x,
                        ln_y,
                        ln_z,
                    )
                )
                missionlist.append(cmd)
    return missionlist


def prepare_dummy_data():
    current_time = get_current_time()
    randf1 = round(random.uniform(50, 100), 2)
    randf11 = round(random.uniform(0, 20), 2)
    randf111 = round(random.uniform(-60, 60), 2)
    randf2 = random.uniform(-0.02, 0.02)
    randf22 = round(random.uniform(0, 1000))
    randf222 = round(random.uniform(0, 10))
    randf3 = random.uniform(-5, 5)
    randint1 = random.randint(0, 1)
    gnss_fix1 = random.randint(0, 2)
    mode1 = random.randint(0, 3)

    rate1 = {
        "rate": database.DroneRates.RATE1,
        "vals": {
            "m_time": current_time,
            "home_lat": 33.21534,
            "home_lon": -87.54355,
            "home_alt": 170,
            "voltage": randf1,
            "current": randf1,
        },
    }
    rate2 = {
        "rate": database.DroneRates.RATE2,
        "vals": {
            "m_time": current_time,
            "latitude": 33.21534 + randf2,
            "longitude": -87.54355 + randf2,
            "relative_alt": randf1,
            "yaw": randf22,
            "heading": randf22 + 20,
            "gnss_fix": mode1,
            "satellites_visible": randf11,
            "roll_angle": randf11,
            "pitch_angle": randf11,
            "alpha": randf3,
            "beta": randf3,
            "airspeed": randf1,
            "gndspeed": randf1,
            "vspeed": randf111,
            "throttle": randf1,
        },
    }
    rate3 = {
        "rate": database.DroneRates.RATE3,
        "vals": {
            "m_time": current_time,
            "chancount": randf11,
            "chan1_raw": randf22,
            "chan2_raw": randf22,
            "chan3_raw": randf22,
            "chan4_raw": randf22,
            "chan5_raw": randf22,
            "chan6_raw": randf22,
            "chan7_rachange the curw": randf22,
            "chan8_raw": randf22,
            "chan9_raw": randf22,
            "chan10_raw": randf22,
            "chan11_raw": randf22,
            "chan12_raw": randf22,
            "chan13_raw": randf22,
            "chan14_raw": randf22,
            "chan16_raw": randf22,
            "chan17_raw": randf22,
            "chan18_raw": randf22,
            "rssi": randf1,
            "servo_port": randf222,
            "servo1_raw": randf22,
            "servo2_raw": randf22,
            "servo3_raw": randf22,
            "servo4_raw": randf22,
            "servo5_raw": randf22,
            "servo6_raw": randf22,
            "servo7_raw": randf22,
            "servo8_raw": randf22,
            "servo9_raw": randf22,
            "servo10_raw": randf22,
            "servo11_raw": randf22,
            "servo12_raw": randf22,
            "servo13_raw": randf22,
            "servo14_raw": randf22,
            "servo15_raw": randf22,
            "servo16_raw": randf22,
        },
    }
    rate4 = {
        "rate": database.DroneRates.RATE4,
        "vals": {
            "m_time": current_time,
            "armed": random.choice([0, 1]),
            "flight_mode": random.choice(["STABILIZE", "GUIDED", "AUTO", "RTL"]),
            "mav_type": 2,
            "autopilot": 1,
            "custom_mode": 0,
            "tof": randf222,
            "next_wp": randf222,
            "relay_sw": randint1,
            "engine_sw": randint1,
        },
    }
    all_data = rate1, rate2, rate3, rate4
    return all_data


def prepare_data_from_mavlink(radio, name, port, rate1, rate2, rate3, rate4, data):
    current_time = get_current_time()

    data["MAV"] = {}
    data["ATTITUDE"] = {}
    data["VFR_HUD"] = {}
    # data['HEARTBEAT'] = {}
    # data['HOME'] = {}
    data["LOCAL_POSITION_NED"] = {}
    data["GLOBAL_POSITION_INT"] = {}
    data["BATTERY_STATUS"] = {}
    data["GPS_RAW_INT"] = {}

    # populating data{} before writing rates for database
    data["MAV"]["armed"] = int(radio.armed)
    data["MAV"]["base_mode"] = radio.mode.name
    data["MAV"]["flight_mode"] = radio.mode.name
    data["MAV"]["mav_type"] = 0
    data["MAV"]["next_wp"] = radio.commands.next
    data["vehicle_type"] = radio._vehicle_type

    data["ATTITUDE"]["roll"] = radio.attitude.roll * r2d
    data["ATTITUDE"]["pitch"] = radio.attitude.pitch * r2d

    data["VFR_HUD"]["yaw"] = radio.attitude.yaw * r2d
    data["VFR_HUD"]["airspeed"] = radio.airspeed
    data["VFR_HUD"]["groundspeed"] = radio.groundspeed

    data["GLOBAL_POSITION_INT"]["lat"] = radio.location._lat
    data["GLOBAL_POSITION_INT"]["lon"] = radio.location._lon
    data["GLOBAL_POSITION_INT"]["relative_alt"] = radio.location._relative_alt

    data["LOCAL_POSITION_NED"]["vx"] = radio._vx
    data["LOCAL_POSITION_NED"]["vy"] = radio._vy
    data["LOCAL_POSITION_NED"]["heading"] = radio.heading

    data["BATTERY_STATUS"]["voltage"] = radio.battery.voltage
    data["BATTERY_STATUS"]["current"] = radio.battery.current

    data["GPS_RAW_INT"]["fix_type"] = radio._fix_type
    data["GPS_RAW_INT"]["satellites_visible"] = radio._satellites_visible

    # putting zero for things confused from dronekit
    data["VFR_HUD"]["climb"] = 0
    data["VFR_HUD"]["throttle"] = 0

    # populating rate dictionaries from mavlink data
    for rate in (rate1, rate2, rate3, rate4):
        rate["vals"]["m_time"] = current_time

    # Put zero for things not available currently
    rate1["vals"]["home_lat"] = 0
    rate1["vals"]["home_lon"] = 0
    rate1["vals"]["home_alt"] = 0

    rate4["vals"]["tof"] = 0
    rate4["vals"]["relay_sw"] = 0
    rate4["vals"]["engine_sw"] = 0
    rate2["vals"]["alpha"] = 0
    rate2["vals"]["beta"] = 0

    if "MAV" in data:
        rate4["vals"]["flight_mode"] = data["MAV"]["base_mode"]
        rate4["vals"]["mav_type"] = data["MAV"]["mav_type"]
        rate4["vals"]["armed"] = data["MAV"]["armed"]
        rate4["vals"]["next_wp"] = data["MAV"]["next_wp"]

    if "ATTITUDE" in data:
        rate2["vals"]["roll_angle"] = data["ATTITUDE"]["roll"]
        rate2["vals"]["pitch_angle"] = data["ATTITUDE"]["pitch"]

    if "VFR_HUD" in data:
        rate2["vals"]["airspeed"] = round(data["VFR_HUD"]["airspeed"])
        rate2["vals"]["gndspeed"] = round(data["VFR_HUD"]["groundspeed"], 1)
        rate2["vals"]["yaw"] = data["LOCAL_POSITION_NED"]["heading"]
        rate2["vals"]["vspeed"] = round(data["VFR_HUD"]["climb"], 1)
        rate2["vals"]["throttle"] = round(data["VFR_HUD"]["throttle"])

    if "LOCAL_POSITION_NED" in data:
        vx = data["LOCAL_POSITION_NED"]["vx"]
        vy = data["LOCAL_POSITION_NED"]["vy"]
        # rate2['vals']['heading'] = round(math.degrees(math.atan2(vy, vx)))
        rate2["vals"]["heading"] = 0

    if "GLOBAL_POSITION_INT" in data:
        rate2["vals"]["latitude"] = data["GLOBAL_POSITION_INT"]["lat"]
        rate2["vals"]["longitude"] = data["GLOBAL_POSITION_INT"]["lon"]
        rate2["vals"]["relative_alt"] = data["GLOBAL_POSITION_INT"]["relative_alt"]

    if "BATTERY_STATUS" in data:
        rate1["vals"]["voltage"] = data["BATTERY_STATUS"]["voltage"]
        # rate1['vals']['current'] = data['BATTERY_STATUS']['current']
        rate1["vals"]["current"] = 0

    if "GPS_RAW_INT" in data:
        rate2["vals"]["gnss_fix"] = data["GPS_RAW_INT"]["fix_type"]
        rate2["vals"]["satellites_visible"] = data["GPS_RAW_INT"]["satellites_visible"]
    return rate1, rate2, rate3, rate4, data


def check_for_signal(conn, radio):
    if not conn.hasPendingDatagrams():
        return

    data = conn.receiveDatagram(conn.pendingDatagramSize())
    received_signal = json.loads(data.data().data().decode(conn_settings.FORMAT))
    addr = data.senderAddress()
    port = data.senderPort()

    if received_signal["type"] == conn_settings.UPLOAD_WP:
        succ, err = upload_waypoints(received_signal, radio)
        response = {"success": succ, "info": err}

    elif received_signal["type"] == conn_settings.AUTO_CMD:
        succ, err = get_autopilot_command(received_signal, radio)
        response = {"success": succ, "info": err}

    elif received_signal["type"] == conn_settings.DOWNLOAD_WP:
        succ, err = download_and_save_mission(received_signal, radio)
        response = {"success": succ, "info": err}

    else:
        response = {
            "success": False,
            "info": "Signal not recognized by Radio manager.\n Received signal: {}".format(
                str(received_signal)
            ),
        }

    # Sending message back to client socket (Conn-server)
    f_response = json.dumps(response).encode(conn_settings.FORMAT)
    conn.writeDatagram(f_response, addr, port)


def download_mission():
    missionlist = []
    cmds = radio.commands
    cmds.download()
    cmds.wait_ready()
    for cmd in cmds:
        missionlist.append(cmd)
    return missionlist


def download_and_save_mission(received_signal, radio):
    err = ""
    missions = download_mission()
    for cmd in missions:
        cmd_vals = {
            "seq": cmd.seq,
            "current": cmd.current,
            "frame": cmd.frame,
            "command": cmd.command,
            "param1": cmd.param1,
            "param2": cmd.param2,
            "param3": cmd.param3,
            "param4": cmd.param4,
            "x": cmd.x,
            "y": cmd.y,
            "z": cmd.z,
            "autocontinue": cmd.autocontinue,
        }
        table_name = name + "_mission"
        res = database.add_values(cmd_vals, table_name)
        if not res:
            err = "Unable to write waypoint #{} to the database".format(cmd.seq)

    return True, err


def get_autopilot_command(received_signal, radio):

    succ = False
    err = None

    # check the type of autopilot command
    if received_signal["cmd"] == conn_settings.TAKEOFF:
        take_off_alt = int(received_signal["param"])
        logger.info("Taking off to {}m".format(take_off_alt))
        succ, err = take_off(take_off_alt, radio)

    elif received_signal["cmd"] == conn_settings.GOTO_NEXT_WP:
        logger.info("Going to the next waypoint")
        succ, err = goto_next_wp(received_signal, radio)

    elif received_signal["cmd"] == conn_settings.SET_MODE:
        mode = received_signal["param"]
        logger.info("Setting vehicle mode to {}".format(mode))
        radio.mode = dronekit.VehicleMode(mode)
        succ = True, ""
        succ, err = set_mode(mode, radio)

    elif received_signal["cmd"] == conn_settings.ARM_DISARM:
        new_state = bool(int(received_signal["param"]))
        logger.info("Setting armed state to {}".format(new_state))
        succ, err = arm_disarm(new_state, radio)

    return succ, err


def get_current_time():
    return time.time()


def define_parser():
    parser = ArgumentParser(
        description="Process command line options for radio connection"
    )

    default = "DroneX"
    parser.add_argument(
        "--name",
        type=str,
        help="Name of the vehicle. The default is {}".format(default),
        default=default,
    )

    default = "/dev/test/"
    parser.add_argument(
        "--port",
        type=str,
        help="Port of radio connection. The default is {}".format(default),
        default=default,
    )

    default = "red"
    parser.add_argument(
        "--color",
        type=str,
        help="Color for the vehicle's icons. The default is {}".format(default),
        default=default,
    )

    default = 38400
    parser.add_argument(
        "--baud",
        type=int,
        help="Baud rate for radio connection. The default is {}".format(default),
        default=default,
    )

    default = 9830
    parser.add_argument(
        "--udp_port",
        type=str,
        help="Port for UDP socket connection. The default is {}".format(default),
        default=default,
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Run in debug mode",
    )

    return parser


def _cleanup_handler(signum, frame, radio, conn):
    radio.close()
    conn.close()

    os._exit(0)


_handleable_sigs = (
    signal.SIGKILL,
    signal.SIGSEGV,
    signal.SIGTERM,
    signal.SIGINT,
    signal.SIGQUIT,
    signal.SIGSTOP,
)

# %% Main function
if __name__ == "__main__":

    args = define_parser().parse_args()
    name = args.name
    port = args.port
    color = args.color
    baud = args.baud
    udp_port = args.udp_port

    ch = logging.StreamHandler()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[radio-manager] %(levelname)s %(asctime)s - %(message)s"
    )
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    if not database.connect_db():
        logger.critical("Failed to open database")
        sys.exit(-2)

    sig_conn = QtNetwork.QUdpSocket()
    sig_conn.bind(int(udp_port))

    if port == "/dev/test/":
        logger.debug("Connected to test port")
        while True:
            check_for_signal(sig_conn, None)
            all_data = prepare_dummy_data()
            res = database.write_values(all_data, name)
            time.sleep(0.2)

    else:
        try:
            radio = dronekit.connect(port, wait_ready=True)
        except:
            sys.exit(-1)

        for sig in _handleable_sigs:
            try:
                signal.signal(
                    sig,
                    lambda signum, frame: _cleanup_handler(
                        signum, frame, radio, sig_conn
                    ),
                )
            except (ValueError, OSError):
                continue

        mav_data = {}
        all_data = prepare_dummy_data()
        res = database.write_values(all_data, name)

        rate1, rate2, rate3, rate4 = [all_data[i] for i in range(len(all_data))]

        while True:
            check_for_signal(sig_conn, radio)
            (rate1, rate2, rate3, rate4, mav_data,) = prepare_data_from_mavlink(
                radio, name, port, rate1, rate2, rate3, rate4, mav_data
            )
            all_data = rate1, rate2, rate3, rate4
            res = database.write_values(all_data, name)
            time.sleep(0.075)

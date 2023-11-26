"""GUST plugin for Radio Manager."""

import math
import random
import time
import numpy as np
import logging
import sys
import signal
import os
import json
from argparse import ArgumentParser

import dronekit
from PyQt5 import QtNetwork

import utilities.database as database
from utilities import ConnSettings as conn_settings
from radio_manager import logger

d2r = np.pi / 100
r2d = 1 / d2r

# Update rates in Hz.
_DUMMY_DATA_UPDATE_RATE = 5
_MAV_RADIO_UPDATE_RATE = 15

#################
# Dronekit's API Reference:
# https://dronekit-python.readthedocs.io/en/latest/automodule.html
#################


# %% Custom Functions


def get_distance_metres(aLocation1, aLocation2):
    """
    Get the distance between two positions.

    Parameters
    ----------
    aLocation1: dronekit's `LocationGlobal` or `LocationGlobalRelative` object

    aLocation2: dronekit's `LocationGlobal` or `LocationGlobalRelative` object

    Returns
    -------
    d: float
        Distance between two positions in metres

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
    Find the distance of the vehicle from the next waypoint in the mission.

    Parameters
    ----------
    radio: dronekit's Vehicle object

    Returns
    -------
    distancetopoint: float
        Distance of the vehicle to the next waypoint.

    """

    # Finding the next waypoint in the mission
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


def goto_next_wp(radio):
    """
    Command the vehicle to proceed to the next waypoint

    Parameters
    ----------
    radio: dronekit's Vehicle object

    Returns
    -------
    succ: bool
        Success of the command
    err: str
        Response of the command (usually error message)

    """
    radio.commands.next = radio.commands.next + 1
    succ = True
    err = "Going to wp: {}".format(radio.commands.next)
    return succ, err


def goto_set_wp(wp_num, radio):
    """
    Command the vehicle to proceed to the given waypoint

    Parameters
    ----------
    wp_num: int
        Next Waypoint for the vehicle in AUTO mode
    radio: dronekit's Vehicle object

    Returns
    -------
    succ: bool
        Success of the command
    err: str
        Response of the command (usually error message)

    """
    radio.commands.next = wp_num
    succ = True
    err = "Going to wp: {}".format(radio.commands.next)
    return succ, err


def set_mode(mode, radio):
    """
    Change the flight mode of the vehicle to mode.

    Parameters
    ----------
    mode: str
        Flight Mode of the vehicle. See Dronekit's API reference for available
        flight modes.
    radio: dronekit's Vehicle object

    Returns
    -------
    succ: bool
        Success of the command
    err: str
        Response of the command (usually error message)
    """
    radio.mode = dronekit.VehicleMode(mode)
    succ = True
    err = ""
    return succ, err


def take_off(take_off_alt, radio):
    """
    Send a take-off command to the vehicle. Fails if the vehicle is not already armed.

    Parameters
    ----------
    take_off_alt: int
        Take-off altitude
    radio: dronekit's Vehicle object

    Returns
    -------
    succ: bool
        Success of the command
    err: str
        Response of the command (usually error message)
    """

    logger.info("Basic pre-arm checks")
    while not radio.is_armable:
        logger.info("waiting for vehicle to initialize")
        time.sleep(1)

    if not radio.armed:
        return False, "Vehicle is not armed."

    logger.info("Vehicle is armed.")
    logger.info("Changing flight mode to GUIDED")
    radio.mode = dronekit.VehicleMode("GUIDED")

    logger.info("Taking off...")
    radio.simple_takeoff(take_off_alt)
    succ = True
    err = ""
    return succ, err


def arm_disarm(bool_val, radio):
    """
    Change the arm state of the vehicle.

    Parameters
    ----------
    bool_val: bool
        True for arming and False for disarming.
    radio: dronekit's Vehicle object

    Returns
    -------
    succ: bool
        Success of the command
    err: str
        Response of the command (usually error message)
    """
    if radio.armed is not bool_val:
        radio.armed = bool_val
        succ = True
        err = " "
    else:
        succ = False
        err = "Armed state is already {}".format(bool_val)
    return succ, err


def upload_waypoints(received_signal, radio):
    """
    Uploads a mission to the vehicle

    Parameters
    ----------
    received_signal: dict
        Main received signal from ConnServer. Includes path for the mission file.
    radio: dronekit's Vehicle object.

    Returns
    -------
    succ: bool
        Success of the command
    err: str
        Response of the command (usually error message)
    """

    # filepath for the mission file.
    filename = received_signal["filename"]

    # a list of mission items (dronekit.Command objects)
    missionList = readmission(filename, radio)
    logger.info("Uploading waypoints from {}\n".format(filename))

    # clearing the current mission from the vehicle.
    logger.info("Clearing older mission\n")
    cmds = radio.commands
    cmds.clear()
    cmds.upload()

    # Uploading each waypoint
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
    Read the mission file and prepare to be uploaded to the vehicle.
    The file is formatted as a regular Mission (waypoint) file.
    This file should be compatible with Mission Planner and QGC.

    Parameters
    ----------
    filename: str
        Path of the mission file
    radio: dronekit's Vehicle object

    Returns
    -------
    missionlist: list
        List of dronekit.Command objects. Each item of missionlist can be directly
        uploaded to the vehicle.
    """

    logger.info("Reading mission from file: {}\n".format(filename))
    cmds = radio.commands
    missionlist = []
    with open(filename) as f:
        for i, line in enumerate(f):
            if i == 0:
                # Make sure the waypoint file has the correct format
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

                # creating a dronekit.Command object for each line in the mission file.
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


def download_mission():
    """Download dronekit.Command objects from the vehicle's mission."""

    missionlist = []
    cmds = radio.commands
    cmds.download()
    cmds.wait_ready()
    # cmd is the dronekit.Command object in the vehicle.
    for cmd in cmds:
        missionlist.append(cmd)
    return missionlist


def download_and_save_mission(received_signal, radio):
    """
    Download missions from the vehicle and save in the database.

    Parameters
    ----------
    received_signal: dict
        Main message coming from the ConnServer
    radio: dronekit's Vehicle Object

    Returns
    -------
    succ: bool
        Success of the command
    err: str
        Response of the command (usually error message)
    """
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
        # writing the mission items in the database.
        table_name = name + "_mission"
        res = database.add_values(cmd_vals, table_name)
        if not res:
            err = "Unable to write waypoint #{} to the database".format(cmd.seq)
    return True, err


def prepare_dummy_data():
    """
    Prepare a set of dummy MAVLink data. Used for a dummy test connection.
    The data is divided into different rates. More info on this can be found on the
    docs or in the database file.
    The rate key in each dict stores a Enum (defined in database).

    Returns
    -------
    all_data: tuple
        Tuple of all rate dicts.
    """
    current_time = get_current_time()
    randf1 = round(random.uniform(50, 100), 2)
    randf11 = round(random.uniform(0, 20), 2)
    randf111 = round(random.uniform(-60, 60), 2)
    randf2 = random.uniform(-0.02, 0.02)
    randf22 = round(random.uniform(0, 1000))
    randf222 = round(random.uniform(0, 10))
    randf3 = random.uniform(-5, 5)
    randint1 = random.randint(0, 1)
    gnss_fix1 = random.randint(1, 5)

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
            "gnss_fix": gnss_fix1,
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
            "ekf_ok": random.choice([0, 1]),
            "vehicle_type": 13,
            "sys_status": "STANDBY",
            "tof": randf222,
            "next_wp": randf222,
            "relay_sw": randint1,
            "engine_sw": randint1,
        },
    }
    all_data = rate1, rate2, rate3, rate4
    return all_data


def prepare_data_from_mavlink(radio, rate1, rate2, rate3, rate4):
    """Populate the rate dicts with vehicle state using dronekit.
    Ref:: https://dronekit-python.readthedocs.io/en/latest/guide/vehicle_state_and_parameters.html
    """

    current_time = get_current_time()
    for rate in (rate1, rate2, rate3, rate4):
        rate["vals"]["m_time"] = current_time

    ##########
    # RATE-1
    ##########
    if radio._home_location is not None:
        rate1["vals"]["home_lat"] = radio.home_location.lat
        rate1["vals"]["home_lon"] = radio.home_location.lon
        rate1["vals"]["home_alt"] = radio.home_location.alt
    else:
        rate1["vals"]["home_lat"] = 0
        rate1["vals"]["home_lon"] = 0
        rate1["vals"]["home_alt"] = 0
    rate1["vals"]["voltage"] = radio.battery.voltage
    rate1["vals"]["current"] = radio.battery.current

    ##########
    # RATE-2
    ##########
    # Attitude
    rate2["vals"]["roll_angle"] = round(radio.attitude.roll * r2d, 1)
    rate2["vals"]["pitch_angle"] = round(radio.attitude.pitch * r2d, 1)
    # VFR HUD
    rate2["vals"]["airspeed"] = round(radio.airspeed, 1)
    rate2["vals"]["gndspeed"] = round(radio.groundspeed, 1)
    rate2["vals"]["yaw"] = radio.heading
    rate2["vals"]["vspeed"] = radio.velocity[2]
    rate2["vals"]["latitude"] = radio.location.global_relative_frame.lat
    rate2["vals"]["longitude"] = radio.location.global_relative_frame.lon
    # this altitude is relative to the take off area
    rate2["vals"]["relative_alt"] = radio.location.global_relative_frame.alt
    rate2["vals"]["gnss_fix"] = radio.gps_0.fix_type
    rate2["vals"]["satellites_visible"] = radio.gps_0.satellites_visible
    # heading
    vx = radio.velocity[0]
    vy = radio.velocity[1]
    rate2["vals"]["heading"] = round(r2d * math.atan2(vy, vx), 1)

    ##########
    # RATE-3
    ##########
    # Don't care about this right now.

    ##########
    # RATE-4
    ##########
    rate4["vals"]["flight_mode"] = radio.mode.name
    rate4["vals"]["armed"] = int(radio.armed)
    rate4["vals"]["next_wp"] = radio.commands.next
    rate4["vals"]["ekf_ok"] = int(radio.ekf_ok)
    rate4["vals"]["vehicle_type"] = radio.version.vehicle_type
    rate4["vals"]["sys_status"] = radio.system_status.state
    # Currently all zero.
    rate4["vals"]["tof"] = 0
    rate4["vals"]["relay_sw"] = 0
    rate4["vals"]["engine_sw"] = 0

    # Things I am not sure about currently
    rate2["vals"]["throttle"] = 0
    rate2["vals"]["alpha"] = 0
    rate2["vals"]["beta"] = 0

    return rate1, rate2, rate3, rate4


def check_for_signal(conn, radio):
    """Check if any message is received in the UDP socket. Messages are expected to
    come from ConnServer"""

    # Do nothing if there is no new messages.
    if not conn.hasPendingDatagrams():
        return

    # decoding the messages into nice formats (Similar to ConnServer.)
    data = conn.receiveDatagram(conn.pendingDatagramSize())
    received_signal = json.loads(data.data().data().decode(conn_settings.FORMAT))
    addr = data.senderAddress()
    port = data.senderPort()

    # Check if the radio connection is valid
    if radio is not None:
        # Check the message type
        if received_signal["type"] == conn_settings.UPLOAD_WP:
            succ, err = upload_waypoints(received_signal, radio)
            response = {"success": succ, "info": err}

        # All autopilot commands are lumped into one and is handled by
        # get_autopilot_command()
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

    else:
        response = {"success": False, "info": "Not a MAVLink connection."}

    # Sending message back to client socket (Conn-server)
    f_response = json.dumps(response).encode(conn_settings.FORMAT)
    conn.writeDatagram(f_response, addr, port)


def get_autopilot_command(received_signal, radio):
    """Handles relay of all the autopilot related commands to the radio."""
    succ = False
    err = None

    # check the type of autopilot command
    if received_signal["cmd"] == conn_settings.TAKEOFF:
        take_off_alt = int(received_signal["param"])
        logger.info("Taking off to {}m".format(take_off_alt))
        succ, err = take_off(take_off_alt, radio)

    elif received_signal["cmd"] == conn_settings.GOTO_NEXT_WP:
        next_wp = int(received_signal["param"])
        logger.info("Going to the waypoint {}".format(next_wp))
        succ, err = goto_set_wp(next_wp, radio)

    elif received_signal["cmd"] == conn_settings.SET_MODE:
        mode = received_signal["param"]
        logger.info("Setting vehicle mode to {}".format(mode))
        succ, err = set_mode(mode, radio)

    elif received_signal["cmd"] == conn_settings.ARM_DISARM:
        new_state = bool(int(received_signal["param"]))
        logger.info("Setting armed state to {}".format(new_state))
        succ, err = arm_disarm(new_state, radio)

    return succ, err


def get_current_time():
    return time.time()


def define_parser():
    """Defining arguments that can be passed to RadioManager process."""
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
    baudrate = args.baud
    udp_port = args.udp_port

    # Handling all the logging stuff
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

    # Connecting to the database
    if not database.connect_db():
        logger.critical("Failed to open database")
        sys.exit(-2)

    # Opening a UDP socket to receive messages from the ConnServer.
    sig_conn = QtNetwork.QUdpSocket()
    sig_conn.bind(int(udp_port))

    # For a test port, just populate some fake data from prepare_dummy_data().
    if port == "/dev/test/":
        logger.debug("Connected to test port")
        while True:
            check_for_signal(sig_conn, None)
            all_data = prepare_dummy_data()
            res = database.write_values(all_data, name)
            time.sleep(1 / _DUMMY_DATA_UPDATE_RATE)

    else:
        try:
            # connect to MAVLink using dronekit.
            radio = dronekit.connect(
                port, baud=baudrate, timeout=200, heartbeat_timeout=200, wait_ready=True
            )
        except:
            sys.exit(-1)

        # Catch any external signals (to kill.)
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

        # using some dummy data for the first timestep and write that to database.
        all_data = prepare_dummy_data()
        res = database.write_values(all_data, name)

        # arranging the rate dicts properly.
        rate1, rate2, rate3, rate4 = [all_data[i] for i in range(len(all_data))]

        # Main Loop for retrieving MAVLink telemetry data
        while True:
            # Checking messages on UDP socket
            check_for_signal(sig_conn, radio)

            # populating rate data
            (rate1, rate2, rate3, rate4) = prepare_data_from_mavlink(
                radio, rate1, rate2, rate3, rate4
            )
            all_data = rate1, rate2, rate3, rate4

            # Writing to the database
            res = database.write_values(all_data, name)

            # 25Hz just considering the sleep time.
            time.sleep(1 / _MAV_RADIO_UPDATE_RATE)

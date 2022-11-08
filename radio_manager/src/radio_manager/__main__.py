"""GUST plugin for <NAME>."""
import argparse
import socket
import json
import dronekit
import random, time
import numpy as np
import gust.database as database

d2r = np.pi / 100
r2d = 1 / d2r

# from <NAME>.schema import validate_data_with_schema, load_schema

# <IMPORTS>


# %% Internal global variables
_ID = None
_PORT = 9500

_SOCKET = None
_SOCK_TIMEOUT = 1

# %% Predefined functions (do not modify)
def __parse_cmd_args():
    """Parse the command line arguments.

    This parses the required commandline arguements, sets the appropriate
    global variables, and provides a help menu. These should not need to be
    changed.

    Returns
    -------
    None.
    """
    global _ID, _PORT

    parser = argparse.ArgumentParser(description='GUST plugin for <NAME>')

    parser.add_argument('id', type=int, help='Unique id for this plugin instance.')
    parser.add_argument('--port', '-p', type=int, help='Port to send data on.',
                        default=_PORT)

    args = parser.parse_args()

    _ID = args.id
    _PORT = args.port


def __format_udp_packet(data_dict, schema):
    """Formats the data as a UDP packet readable by the gust backend application.

    This should not be modified, the gust backend requires a known format for
    the packets received.

    Parameters
    ----------
    *data : iterable
        Each element must be a primitive type; either string, int, or float.

    Raises
    ------
    RuntimeError
        If an unsupported type is found in the data.

    Returns
    -------
    bytes
        Properly encoded packet of data for sending over a UDP socket.
    """
    msg = {'plugin_name': '<NAME>', 'id': int(_ID), 'data': data_dict}

    packet, passed = validate_data_with_schema(msg, schema)
    return json.dumps(packet).encode('utf-8')


def send_data(data_dict, schema):
    """Sends data over a UDP socket to the gust backend.

    This function can be used as is and does not need to be modified.

    Parameters
    ----------
    *data : iterable
        Each element must be a primitive type; either string, int, or float..

    Returns
    -------
    success : bool
        Flag indicating if the data was sent properly.
    """
    global _SOCKET

    success = False

    if _SOCKET is None:
        _SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _SOCKET.settimeout(_SOCK_TIMEOUT)

    packet = __format_udp_packet(data_dict, schema)

    try:
        _SOCKET.sendto(packet, ('127.0.0.1', _PORT))
        success = True

    except socket.error as msg:
        print('Error Code : {:s}\nMessage: {:s}'.format(str(msg[0]), msg[1]))

    except RuntimeError:
        pass

    return success


# %% Custom Functions

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
            "chan7_raw": randf22,
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
            "flight_mode": random.choice(['STABILIZE', 'GUIDED', 'AUTO', 'RTL']),
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

    data['MAV'] = {}
    data['ATTITUDE'] = {}
    data['VFR_HUD'] = {}
    # data['HEARTBEAT'] = {}
    # data['HOME'] = {}
    data['LOCAL_POSITION_NED'] = {}
    data['GLOBAL_POSITION_INT'] = {}
    data['BATTERY_STATUS'] = {}
    data['GPS_RAW_INT'] = {}


    # populating data{} before writing rates for database
    data['MAV']['armed'] = int(radio.armed)
    data['MAV']['base_mode'] = radio.mode.name
    data['MAV']['flight_mode'] = radio.mode.name
    data['MAV']['mav_type'] = 0
    data['vehicle_type'] = radio._vehicle_type

    data['ATTITUDE']['roll'] = radio.attitude.roll * r2d
    data['ATTITUDE']['pitch'] = radio.attitude.pitch * r2d

    data['VFR_HUD']['yaw'] = radio.attitude.yaw * r2d
    data['VFR_HUD']['airspeed'] = radio.airspeed
    data['VFR_HUD']['groundspeed'] = radio.groundspeed

    data['GLOBAL_POSITION_INT']['lat'] = radio.location._lat
    data['GLOBAL_POSITION_INT']['lon'] = radio.location._lon
    data['GLOBAL_POSITION_INT']['relative_alt'] = radio.location._relative_alt

    data['LOCAL_POSITION_NED']['vx'] = radio._vx
    data['LOCAL_POSITION_NED']['vy'] = radio._vy
    data['LOCAL_POSITION_NED']['heading'] = radio.heading

    data['BATTERY_STATUS']['voltage'] = radio.battery.voltage
    data['BATTERY_STATUS']['current'] = radio.battery.current

    data['GPS_RAW_INT']['fix_type'] = radio._fix_type
    data['GPS_RAW_INT']['satellites_visible'] = radio._satellites_visible

    # putting zero for things confused from dronekit
    data['VFR_HUD']['climb'] = 0
    data['VFR_HUD']['throttle'] = 0

    # populating rate dictionaries from mavlink data
    for rate in (rate1, rate2, rate3, rate4):
        rate["vals"]["m_time"] = current_time

    # Put zero for things not available currently
    rate1["vals"]["home_lat"] = 0
    rate1["vals"]["home_lon"] = 0
    rate1["vals"]["home_alt"] = 0

    rate4["vals"]["tof"] = 0
    rate4["vals"]["next_wp"] = 0
    rate4["vals"]["relay_sw"] = 0
    rate4["vals"]["engine_sw"] = 0
    rate2['vals']['alpha'] =0
    rate2['vals']['beta'] = 0


    if "MAV" in data:
        rate4["vals"]["flight_mode"] = data["MAV"]["base_mode"]
        rate4["vals"]["mav_type"] = data["MAV"]["mav_type"]
        rate4["vals"]["armed"] = data["MAV"]["armed"]

    if "ATTITUDE" in data:
        rate2['vals']['roll_angle'] = data['ATTITUDE']['roll']
        rate2['vals']['pitch_angle'] = data['ATTITUDE']['pitch']

    if 'VFR_HUD' in data:
        rate2['vals']['airspeed'] = round(data['VFR_HUD']['airspeed'])
        rate2['vals']['gndspeed'] = round(data['VFR_HUD']['groundspeed'], 1)
        rate2['vals']['yaw'] = round(data['VFR_HUD']['yaw'])
        rate2['vals']['vspeed'] = round(data['VFR_HUD']['climb'], 1)
        rate2['vals']['throttle'] = round(data['VFR_HUD']['throttle'])

    if 'LOCAL_POSITION_NED' in data:
        vx = data['LOCAL_POSITION_NED']['vx']
        vy = data['LOCAL_POSITION_NED']['vy']
        # rate2['vals']['heading'] = round(math.degrees(math.atan2(vy, vx)))
        rate2['vals']['heading'] = 0

    if 'GLOBAL_POSITION_INT' in data:
        rate2['vals']['latitude'] = data['GLOBAL_POSITION_INT']['lat']
        rate2['vals']['longitude'] = data['GLOBAL_POSITION_INT']['lon']
        rate2['vals']['relative_alt'] = data['GLOBAL_POSITION_INT']['relative_alt']

    if 'BATTERY_STATUS' in data:
        rate1['vals']['voltage'] = data['BATTERY_STATUS']['voltage']
        # rate1['vals']['current'] = data['BATTERY_STATUS']['current']
        rate1['vals']['current'] = 0

    if 'GPS_RAW_INT' in data:
        rate2['vals']['gnss_fix'] = data['GPS_RAW_INT']['fix_type']
        rate2['vals']['satellites_visible'] = data['GPS_RAW_INT']['satellites_visible']
    return rate1, rate2, rate3, rate4, data


def get_current_time():
    return time.time()



# %% Main function
def main():
    __parse_cmd_args()
    schema = load_schema('<NAME>_schema.json')

    # get msg from conn_server using socket
    # setup socket for receiving message from conn_server
    received_info = {}

    # similar to poll_radio
    name = received_info["name"]
    port = received_info["port"]
    color = received_info["color"]
    baud = received_info["baud"]


    # or maybe throw this in the conn_server side
    msg = "Connecting to {} on {}".format(name, port)

    if port == '/dev/test/':
        # PROBABLY COULD SOME SORT OF CONDITION TO CHECK CONNECTION?
        while True:
            all_data = prepare_dummy_data()
            res = database.write_values(all_data, name)
            time.sleep(0.2)

    else:

        # setting up the connection with mavlink
        try:
            radio = dronekit.connect(port, wait_ready=True, baud=baud)
        except:
            # RETURN SOMETHING TO CONN_SERVER SAYING THAT ITS NOT CONNECTED
            # msg = {'success': False, 'info': Unable to connect to radio}
            pass

        mav_data = {}
        all_data = prepare_dummy_data()
        res = database.write_values(all_data, name)

        rate1, rate2, rate3, rate4 = [all_data[i] for i in range(len(all_data))]

        # SOME CONDITION HERE? TO CHECK CONNECTION
        while True:
            rate1, rate2, rate3, rate4, mav_data = prepare_data_from_mavlink(
                radio, name, port, rate1, rate2, rate3, rate4, mav_data
                )
            all_data = rate1, rate2, rate3, rate4
            res = database.wrte_values(all_data, name)
            time.sleep(0.075)



# %% Entry Point
main()

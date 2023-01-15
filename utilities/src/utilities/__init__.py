"""Handles data passing between wsgi app and worker threads."""
import socket
import json


class ConnSettings:
    IP = "127.0.0.1"
    PORT = 9810
    FORMAT = 'utf-8'
    MAX_CONNECTIONS = 10
    MAX_MSG_SIZE = 1500
    TIMEOUT = 10

    # DRONE message_type
    DRONE_CONN = 'drone_connect'
    DRONE_DISC = 'drone_disconnect'
    UPLOAD_WP = 'upload_waypoints'
    GOTO_NEXT_WP = 'goto_next_waypoint'
    RADIO_PORTS = [9820, 9825, 9830, 9835, 9840, 9850, 9855, 9860, 9865]

    # CMR Process
    CMR_PORT = 9880
    START_CMR = 'start_cmr_process'
    STOP_CMR = 'stop_cmr_process'

    # ZED message_type
    ZED_CONN = 'zed_connect'
    ZED_DIS_CONN = 'zed_disconnect'

    @classmethod
    def ADDR(cls):
        return cls.IP, cls.PORT

    @classmethod
    def RADIO_UDP_ADDR(cls, port):
        return cls.IP, port

def send_info_to_udp_server(info_dict, msg_type, server_addr=ConnSettings.ADDR()):
    """Packages and sends information to UDP servers as a UDP socket client.

    Parameters
    ----------
    info_dict : dict
        Information to be sent to UDP socket server
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
    client.settimeout(ConnSettings.TIMEOUT)

    msg = {"type": msg_type}
    msg.update(info_dict)

    f_msg = json.dumps(msg).encode(ConnSettings.FORMAT)
    client.sendto(f_msg, server_addr)

    # Try to receive data being sent back from conn_server
    try:
        response, addr = client.recvfrom(ConnSettings.MAX_MSG_SIZE)
        msg = json.loads(response.decode(ConnSettings.FORMAT))
        return msg["success"], msg["info"]

    except socket.timeout:
        msg = "Timeout on connection with backend"
        return False, msg
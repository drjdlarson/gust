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

    # ZED message_type
    ZED_CONN = 'zed_connect'

    @classmethod
    def ADDR(cls):
        return cls.IP, cls.PORT


def send_info_to_conn_server(info_dict, msg_type):
    """Packages and sends information to conn_server as a UDP socket client.

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
    client.settimeout(ConnSettings.TIMEOUT)

    msg = {"type": msg_type}
    msg.update(info_dict)

    f_msg = json.dumps(msg).encode(ConnSettings.FORMAT)
    client.sendto(f_msg, ConnSettings.ADDR())

    # Try to receive data being sent back from conn_server
    try:
        response, addr = client.recvfrom(ConnSettings.MAX_MSG_SIZE)
        msg = json.loads(response.decode(ConnSettings.FORMAT))
        return msg["success"], msg["info"]

    except socket.timeout:
        msg = "Timeout on connection with backend"
        return False, msg

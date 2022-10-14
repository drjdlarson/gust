"""Handles data passing between wsgi app and worker threads."""
import socket
import json

import gust.conn_manager.conn_settings as conn_settings


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

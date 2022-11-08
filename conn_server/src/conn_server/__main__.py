"""GUST plugin for <NAME>."""
import argparse
import socket
import json

from <NAME>.schema import validate_data_with_schema, load_schema

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
# <CODE>


# %% Main function
def main():
    __parse_cmd_args()
    schema = load_schema('<NAME>_schema.json')

    # %%% Custom Code
    # <CODE>



# %% Entry Point
main()

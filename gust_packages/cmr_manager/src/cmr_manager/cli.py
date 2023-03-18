"""GUST plugin for CMR Manager"""

import sys, os, signal
import logging

from argparse import ArgumentParser
from PyQt5 import QtNetwork

import utilities.database as database
from utilities import ConnSettings as conn_settings
from utilities import send_info_to_udp_server

from cmr_manager import logger


def define_parser():
    parser = ArgumentParser(description="Process command line options for CMR Manager")

    default = '9850'
    parser.add_argument(
        "--port",
        type=str,
        help="Port for CMR manager process. The default is {}".format(default),
        default=default
        )

    default = '127.0.0.1'
    parser.add_argument(
        "--ip",
        type=str,
        help="IP for CMR manager process. The default is {}".format(default),
        default=default,
        )

    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Run in debug mode",
    )

    return parser

def _cleanup_handler(signum, frame, conn):
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

if __name__ == "__main__":

    args = define_parser().parse_args()
    cmr_ip = args.ip
    cmr_port = args.port

    sig_conn = QtNetwork.QUdpSocket()
    sig_conn.bind(int(cmr_port))

    ch = logging.StreamHandler()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        ch.setLevel(logging.INFO)

    formatter = logging.Formatter('[CMR_manager] %(levelname)s %(asctime)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    if not database.connect_db():
        sys.exit(-2)
    names = database.get_drone_ids()



    # just verifying next waypoint signal
    next_wp_info = {'name': names[0], 'next_wp': 4, 'extra': 'random msg from cmr backend'}
    succ, info = send_info_to_udp_server(next_wp_info, conn_settings.GOTO_NEXT_WP)

    if succ:
        database.add_vehicle("Works", '/dev/ttyifbas/', 'green')
    else:
        database.add_vehicle("Doesnt work", '/dev/ttysfas', 'black')

    for sig in _handleable_sigs:
        try:
            signal.signal(sig, lambda signum, frame: _cleanup_handler(signum, frame))
        except (ValueError, OSError):
            continue

    while True:
        # put all the stuff here
        pass
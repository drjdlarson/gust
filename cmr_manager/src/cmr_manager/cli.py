"""GUST plugin for CMR Manager"""

import sys, os, signal
from argparse import ArgumentParser
import utilities.database as database

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

    return parser

def _cleanup_handler(signum, frame, proc):
    proc.close()
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

    # get cmr vehicles from the database


    if not database.connect_db():
        sys.exit(-2)
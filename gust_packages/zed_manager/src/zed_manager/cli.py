"""Entry point of zed-manager process: Handles communication with Zed."""
import sys
import signal
import time
import logging
from argparse import ArgumentParser

from zed import zedManager, logger

import utilities.database as database

RUNNING = True


def define_parser():
    parser = ArgumentParser(
        description="Process command line options for radio connection"
    )

    parser.add_argument(
        "name",
        type=str,
        help="Name of the camera",
    )

    parser.add_argument("filename", type=str, help="Filename of the config file")

    parser.add_argument(
        "hac_dist", type=float, help="Characteristic distance of HA clustering"
    )

    parser.add_argument(
        "update_rate", type=float, help="Update rate for the camera (in sec)"
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Run in debug mode",
    )

    return parser


def _cleanup_handler(signum, frame):
    global RUNNING
    RUNNING = False
    zedManager.shutdown()


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
    filename = args.filename
    hac_dist = args.hac_dist
    update_rate = args.update_rate

    ch = logging.StreamHandler()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[zed-manager] %(levelname)s %(asctime)s - %(message)s"
    )
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    if not database.connect_db():
        logger.critical("Failed to connect to database")
        sys.exit(-2)

    try:
        if not zedManager.connect_to_cameras(filename=filename):
            logger.ciritcal("Failed to connect to cameras")
            zedManager.shutdown()
            sys.exit(-1)

    except:
        zedManager.shutdown()
        logger.error("An exception occured while connecting", stack_info=True)
        sys.exit(-1)

    for sig in _handleable_sigs:
        try:
            signal.signal(sig, _cleanup_handler)
        except (ValueError, OSError):
            logger.debug("Failed to connect signal %d", sig)
            continue

    logger.debug(repr(zedManager.cameras))
    for cam in zedManager.cameras:
        logger.info("Found camera: %s", cam.friendly_name)
    cam = zedManager.cameras[0]
    logger.info("Starting to get ZED measurements...")
    while RUNNING:
        try:
            meas_arr = cam.extract_objects(max_dist=hac_dist)
            posix = time.time()
            if meas_arr.size > 0:
                logger.debug("Extracted: %d objects", meas_arr.shape[0])
                database.write_zed_objs(name, posix, meas_arr)
            else:
                logger.debug("No objects")
        except TypeError:
            logger.warning("Failed to extract/save objects", stack_info=True)
            continue
        time.sleep(update_rate)

    sys.exit(0)
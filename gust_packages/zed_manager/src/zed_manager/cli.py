import os, sys, signal, time
from argparse import ArgumentParser

from zed import zedManager

import utilities.database as database


def define_parser():
    parser = ArgumentParser(description="Process command line options for radio connection")

    parser.add_argument(
        "name",
        type=str,
        help="Name of the camera",
        )

    parser.add_argument(
        "filename",
        type=str,
        help="Filename of the config file"
        )

    parser.add_argument(
        "hac_dist",
        type=float,
        help="Characteristic distance of HA clustering"
        )

    parser.add_argument(
        "update_rate",
        type=int,
        help="Update rate for the camera (in sec)"
        )

    return parser


def _cleanup_handler(signum, frame):
    zedManager.kill()
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
    filename = args.filename
    hac_dist = args.hac_dist
    update_rate = args.update_rate

    if not database.connect_db():
        sys.exit(-2)

    try:
        if not zedManager.connect_to_cameras(filename=filename):
            zedManager.kill()
            sys.exit(-1)

    except:
        zedManager.kill()
        sys.exit(-1)

    for sig in _handleable_sigs:
        try:
            signal.signal(sig, _cleanup_handler)
        except (ValueError, OSError):
            continue

    print(zedManager.cameras)
    for cam in zedManager.cameras:
        print(cam.friendly_name)
    cam = zedManager.cameras[0]
    while True:
        try:
            meas_arr = cam.extract_objects(max_dist=hac_dist)
            posix = time.time()
            for m in meas_arr:
                database.write_zed_obj(name, posix, m)
        except TypeError:
            continue
        time.sleep(update_rate)
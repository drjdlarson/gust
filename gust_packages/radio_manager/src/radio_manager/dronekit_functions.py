import logging, time
import dronekit

logger = logging.getLogger(__name__)


def goto_next_wp(received_signal, radio):
    succ = True
    err = "Next waypoint signal works. {} going to waypoint {}".format(
        received_signal["name"], received_signal["next_wp"]
    )
    return succ, err


def set_mode(received_signal, radio):
    if radio is None:
        succ = False
        err = "Not Connected to radio"
    else:
        mode = received_signal["param"]
        logger.info("Setting vehicle mode to {}".format(mode))
        radio.mode = dronekit.VehicleMode(mode)
        succ = True
        err = ""
    return succ, err


def take_off(received_signal, radio):
    if radio is None:
        succ = False
        err = "Not Connected to radio"
    else:

        logger.info("Basic pre-arm checks")
        while not radio.is_armable:
            logger.info("waiting for vehicle to initialize")
            time.sleep(1)

        logger.info("arming motors")
        radio.mode = dronekit.VehicleMode("GUIDED")
        radio.armed = True

        while not radio.armed:
            logger.info("waiting for arming...")
            time.sleep(1)

        logger.info("Taking off...")
        radio.simple_takeoff(int(received_signal["param"]))
        succ = True
        err = ""
    return succ, err


def upload_waypoints(received_signal, radio):
    """Upload a mission from a file"""
    filename = received_signal["filename"]

    missionList = readmission(filename, radio)
    logger.info("Uploading waypoints from {}\n".format(filename))
    logger.info("Clearing older mission\n")

    cmds = radio.commands
    cmds.clear()
    cmds.upload()

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
    Load a mission from a file into a list.

    This function is used by upload_mission().
    """
    print("Reading mission from file: {}\n".format(filename))
    cmds = radio.commands
    missionlist = []
    with open(filename) as f:
        for i, line in enumerate(f):
            if i == 0:
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

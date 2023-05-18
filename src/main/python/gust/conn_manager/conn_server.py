"""Process for handling multi-process communication and connections"""
import json
import platform
import logging
import time, sys
import random

from PyQt5.QtCore import QProcess, QProcessEnvironment
from PyQt5 import QtNetwork

from utilities import ConnSettings as conn_settings
import utilities.database as database
from utilities import send_info_to_udp_server

logger = logging.getLogger(__name__)
logger.propagate = False


####################
# NOTE: Message types, ports, and other constants are defined in utilities.ConnSettings
####################

class ConnServer:
    """Handles communication and connections between processes"""

    # defining class variables
    running = False
    _cmr_proc = None
    _zeds = None
    _debug = False

    # a dict of connected radios {vehicle_name: Radio's QProcess}
    _radios = {}

    # a dict of running SILs {vehicle_name: SIl's QProcess}
    _sils = {}

    # list of remaining available udp and tcp ports
    # set of predefined ports are listed in conn_settings
    available_udp_ports = []
    available_tcp_ports = []

    # dict of radio process' udp and tcp port
    # {vehicle_name: UDP/TCP port}
    _radio_udp_port = {}
    _sil_tcp_port = {}


    @classmethod
    def start_conn_server(cls, process_events, debug, ctx):
        """
        UDP Socket Server.

        Allow the ConnServer to start listening to socket connection, determine the
        function of the message based on the message type, and pass it to other
        modules/Processes.

        Receives dictionary from the client sockets and sends back dictionary.
        One of the keys in the dictionary is 'type'

        Parameters
        ----------
        process_events
        debug
        ctx

        Returns
        -------

        """
        cls._debug = debug

        # setting up logging stuff
        ch = logging.StreamHandler(stream=sys.stdout)
        if debug:
            logger.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
            ch.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[conn-server] %(levelname)s %(asctime)s - %(message)s"
        )

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        # check if the conn server is already running
        if cls.running:
            logger.warning("Already running!!")
            return
        cls.running = True

        # initially available udp/tcp ports
        cls.available_udp_ports = conn_settings.RADIO_PORTS
        cls.available_tcp_ports = conn_settings.TCP_PORTS

        # creating a UDP socket instance to listen to messages from client sockets
        conn = QtNetwork.QUdpSocket()
        conn.bind(conn_settings.PORT)
        msg = "Listening at {}:{}".format(conn_settings.IP, conn_settings.PORT)
        logger.info(msg)

        # connecting to the database
        if not database.connect_db():
            cls.running = False
            logger.critical("Failed to connect to database, stopping conn_server")

        while cls.running:
            process_events()

            # Receiving message from client socket
            if not conn.hasPendingDatagrams():
                continue

            # decoding the message received from client sockets
            data = conn.receiveDatagram(conn.pendingDatagramSize())
            received_info = json.loads(data.data().data().decode(conn_settings.FORMAT))
            addr = data.senderAddress()
            port = data.senderPort()
            msg = "Message from {} -> {}".format(
                addr.toString().split(":")[-1], received_info
            )
            logger.info(msg)

            ####################
            # Checking message type and forwarding appropriately
            ####################

            # Message for vehicle connection
            if received_info["type"] == conn_settings.DRONE_CONN:
                succ, err = cls.connect_to_radio(received_info, ctx)
                response = {"success": succ, "info": err}

            # Message for vehicle disconnection
            elif received_info["type"] == conn_settings.DRONE_DISC:
                succ, err = cls.disconnect_drone(received_info)
                response = {"success": succ, "info": err}

            # Message for zed connection
            elif received_info["type"] == conn_settings.ZED_CONN:
                succ, err = cls.connect_to_zed(received_info, ctx)
                response = {"success": succ, "info": err}

            # Message for zed disconnection
            elif received_info["type"] == conn_settings.ZED_DIS_CONN:
                succ, err = cls.disconnect_zed(received_info)
                response = {"success": succ, "info": err}

            # Message for autopilot MAVLink command
            elif received_info["type"] == conn_settings.AUTO_CMD:
                succ, err = cls.send_autopilot_commands(received_info)
                response = {"success": succ, "info": err}

            # Message for uploading mission to vehicle
            elif received_info["type"] == conn_settings.UPLOAD_WP:
                succ, err = cls.send_autopilot_commands(received_info)
                response = {"success": succ, "info": err}

            # Message for downloading mission from the vehicle
            elif received_info["type"] == conn_settings.DOWNLOAD_WP:
                succ, err = cls.download_and_save_mission(received_info)
                response = {"success": succ, "info": err}

            # Message for vehicle to proceed to the next waypoint
            elif received_info["type"] == conn_settings.GOTO_NEXT_WP:
                succ, err = cls.send_autopilot_commands(received_info)
                response = {"success": succ, "info": err}

            # Message to start the CMR QProcess
            elif received_info["type"] == conn_settings.START_CMR:
                succ, err = cls.start_cmr_process(ctx)
                response = {"success": succ, "info": err}

            # Message to start the Ardupilot SIL QProcess
            elif received_info["type"] == conn_settings.START_SIL:
                succ, err = cls.start_sil(received_info, ctx)
                response = {"success": succ, "info": err}

            # Message to stop the CMR QProcess
            elif received_info["type"] == conn_settings.STOP_CMR:
                succ, err = cls.stop_cmr_process()
                resposne = {"success": succ, "info": err}

            # Invalid Message type.
            # Check predefined Message types in utilities.ConnSettings
            else:
                response = {
                    "success": False,
                    "info": "Signal not recognized by conn_server. \n Received signal: {}".format(
                        str(received_info)
                    ),
                }

            # Sending a reply back to client socket
            f_response = json.dumps(response).encode(conn_settings.FORMAT)
            conn.writeDatagram(f_response, addr, port)

        logger.info("Closing the conn-server socket")
        conn.close()

    @classmethod
    def kill(cls):
        """Kills all processes related to ConnServer"""

        cls.running = False

        # killing the zed manager process
        if cls._zeds is not None:
            if "windows" in platform.system().lower():
                cls._zeds.kill()
            else:
                cls._zeds.terminate()

            if cls._zeds.state() == QProcess.ProcessState.Running:
                logger.info("Waiting for ZED process to end")
                if not cls._zeds.waitForFinished():
                    logger.critical("Failed to stop zed")
            else:
                logger.info("ZED process not running")

        # killing all the radio manager and SIL processes
        processes = [cls._radios, cls._sils]
        for process in processes:
            for k, p in process.items():
                if "windows" in platform.system().lower():
                    p.kill()
                else:
                    p.terminate()
                if not p.waitForFinished():
                    logger.critical("Failed to end process: %s", k)

    @classmethod
    def connect_to_zed(cls, received_info, ctx):
        """Starts the Zed QProcess"""
        program = ctx.get_resource("zed_manager/zed_manager")
        if cls._debug:
            args = [
                "-d",
            ]
        else:
            args = []
        args.extend(
            [
                received_info["name"],
                received_info["config"],
                str(received_info["hac_dist"]),
                str(received_info["update_rate"]),
            ]
        )
        # Checking if a zed QProcess is already started
        if cls._zeds is not None:
            succ = False
            err = "Zed process already running"
        else:
            cls._zeds = QProcess()
            cls._zeds.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
            cls._zeds.setProcessEnvironment(QProcessEnvironment.systemEnvironment())
            cls._zeds.readyRead.connect(
                lambda: print(cls._zeds.readAllStandardOutput().data().decode().strip())
            )
            cls._zeds.start(program, args)
            logger.info("%s %s", program, " ".join(args))

            succ = cls._zeds.waitForStarted()
            if not succ:
                err = "Failed to start zed process"
                logger.info(err)
                return succ, err
            err = None
        return succ, err

    @classmethod
    def disconnect_zed(cls, received_info):
        """Closes the Zed QProcess"""
        succ = True
        err = ""

        if cls._zeds is not None:
            if cls._zeds.state() == QProcess.ProcessState.Running:
                logger.info("Waiting for ZED process to end")
                if "windows" in platform.system().lower():
                    cls._zeds.kill()
                else:
                    cls._zeds.terminate()

                if not cls._zeds.waitForFinished():
                    logger.critical("Failed to stop zed")
                    succ = False
                    err = "ZED was running but failed to die."
            else:
                logger.info("ZED process not running")

        return succ, err

    @classmethod
    def connect_to_radio(cls, received_info, ctx):
        """
        Starting a Radio Qprocess.

        Parameters
        ----------
        received_info: dict
            Information including vehicle name, port, baud, etc.
            See RadioManager package for more.
        ctx

        Returns
        -------

        """
        err = ""
        name = received_info["name"]
        port_string = received_info["port"]

        # choose a random udp port from available ports to start a radio process on.
        # Each radio process is uniquely identified by the vehicle's name. Each
        # process is tied to a unique UDP port.
        # These processes act like a client sockets and can talk to ConnServer.
        cls._radio_udp_port[name] = random.choice(cls.available_udp_ports)

        # We treat a SIL connection as a regular radio connection.
        # In case of SIL, the port_string is set as "TCP" by the Frontend Window.
        # Here, we simply update the connection port string to include IP and TCP
        # port on which the SIL is running. Each SIL instance is also uniquely
        # identified by the vehicle/SIL name.
        if port_string == "TCP":
            port_string = "tcp:{}:{}".format(conn_settings.IP, cls._sil_tcp_port[name])

        msg = "Connecting to {} on {}: udp connection: {}".format(
            name, port_string, cls._radio_udp_port[name]
        )
        logger.info(msg)

        # RadioManager is a separate GUST package installed and available in the Resources.
        program = ctx.get_resource("radio_manager/radio_manager")
        args = [
            "--name",
            "{}".format(name),
            "--port",
            port_string,
            "--color",
            "{}".format(received_info["color"]),
            "--baud",
            "{}".format(received_info["baud"]),
            "--udp_port",
            "{}".format(str(cls._radio_udp_port[name])),
        ]

        # Check if a radio process is already started with the same name
        if name in cls._radios:
            succ = False
            err = "{} radio process is already running on UDP socket {}".format(
                name, cls._radio_udp_port[name]
            )

        # Starting the Radio Manager Process
        else:
            cls._radios[name] = QProcess()
            cls._radios[name].setProcessChannelMode(
                QProcess.ProcessChannelMode.MergedChannels
            )
            cls._radios[name].setProcessEnvironment(
                QProcessEnvironment.systemEnvironment()
            )
            cls._radios[name].readyRead.connect(
                lambda: print(
                    cls._radios[name].readAllStandardOutput().data().decode().strip()
                )
            )
            cls._radios[name].start(program, args)

            succ = cls._radios[name].waitForStarted()
            if not succ:
                err = "Failed to start Radio process"
                logger.warning(err)
                return succ, err

            # clear the udp port from list of available ports once the process is started
            cls.available_udp_ports.remove(cls._radio_udp_port[name])
        return succ, err

    @classmethod
    def disconnect_drone(cls, received_info):
        """Kills the Radio QProcess for the given drone.
        This stops all communication with the vehicle."""

        name = received_info["name"]

        # Check if a radio process actually exists for the vehicle
        if name in cls._radios:
            if "windows" in platform.system().lower():
                cls._radios[name].kill()
            else:
                cls._radios[name].terminate()
                time.sleep(0.5)
            del cls._radios[name]

            # specify the vehicle as disconnected in the database
            # (without deleting all the flight data)
            database.change_connection_status_value(name, 0)
            cls.available_udp_ports.append(cls._radio_udp_port[name])

            # delete the dict value (Radio QProcess)
            del cls._radio_udp_port[name]

            # Delete the SIL process too, if it exists
            if name in cls._sils:
                if "windows" in platform.system().lower():
                    cls._sils[name].kill()
                else:
                    cls._sils[name].terminate()
                    time.sleep(0.5)
                del cls._sils[name]
                cls.available_tcp_ports.append(cls._sil_tcp_port[name])
                del cls._sil_tcp_port[name]

            succ = True
            err = ""
        else:
            succ = False
            err = "Radio connection not found in conn_server"

        return succ, err

    @classmethod
    def start_sil(cls, received_info, ctx):
        """Start an Ardupilot SIL QProcess"""

        err = ""
        sil_name = received_info["sil_name"]

        # choose a random available TCP port to start a SIL Process
        cls._sil_tcp_port[sil_name] = random.choice(cls.available_tcp_ports)
        msg = "Starting SIL {}: tcp connection: {}".format(
            sil_name, cls._sil_tcp_port[sil_name]
        )
        logger.info(msg)

        # Based on the received_info["vehicle_type"], select the appropriate program to run.
        # Needs an executable program in the Resources for this to run.
        # Currently only supporting Arducopter.
        # See gust/build_scripts/build_sil.h for an example of how to add more.
        # once other SIL executable is added, update the line below to not
        # hardcode "arducopter"
        program = ctx.get_resource("sil_manager/arducopter")
        param_filepath = ctx.get_resource("sil_manager/copter.parm")

        # Starting a SIL process similar to Radio Processes (See above)
        args = [
            "--model",
            "quad",
            "--defaults",
            param_filepath,
            "--autotest-dir",
            ctx.get_resource("sil_manager"),
            "--home",
            received_info["home"],
            "--base-port",
            str(cls._sil_tcp_port[sil_name]),
        ]
        if sil_name in cls._sils:
            succ = False
            err = "{} SIL is already running on TCP {}".format(
                sil_name, cls._sil_tcp_port[sil_name]
            )
        else:
            cls._sils[sil_name] = QProcess()
            cls._sils[sil_name].setProcessChannelMode(QProcess.MergedChannels)
            cls._sils[sil_name].setProcessEnvironment(
                QProcessEnvironment.systemEnvironment()
            )
            cls._sils[sil_name].start(program, args)
            succ = cls._sils[sil_name].waitForStarted()

            if not succ:
                err = "Failed to start SIL"
                logger.warning(err)
                return succ, err

            cls.available_tcp_ports.remove(cls._sil_tcp_port[sil_name])
        return succ, err

    @classmethod
    def send_autopilot_commands(cls, received_info):
        """Sends Autopilot MAVLink command to the specific radio process"""
        logger.info(received_info)

        # Identifying the vehicle for which the command is sent
        name = received_info["name"]

        # finding the UDP port on which that vehicle's Radio Process is running
        udp_port = cls._radio_udp_port[name]

        # sending the message to that UDP port.
        # send_info_to_udp_server() is used for formatting the messages appropriately
        # for socket communication.
        succ, err = send_info_to_udp_server(
            received_info,
            received_info["type"],
            conn_settings.RADIO_UDP_ADDR(udp_port),
        )
        return succ, err

    @classmethod
    def goto_next_waypoint(cls, received_info):
        """Sends Autopilot MAVLink command to proceed to the next waypoint"""

        # Radio Process Id and sending message is similar to send_autopilot_commands()
        # [See above.]
        name = received_info["name"]
        udp_port = cls._radio_udp_port[name]
        succ, err = send_info_to_udp_server(
            received_info,
            conn_settings.GOTO_NEXT_WP,
            conn_settings.RADIO_UDP_ADDR(udp_port),
        )
        return succ, err

    @classmethod
    def download_and_save_mission(cls, received_info):
        """Sends Autopilot MAVLink command to download loaded waypoints from all
        connected vehicles."""
        for name, udp_port in cls._radio_udp_port.items():
            database.remove_older_mission_items(name)

            # Does not need radio process Id since we're downloading missions from
            # all connected vehicles
            succ, err = send_info_to_udp_server(
                {},
                conn_settings.DOWNLOAD_WP,
                conn_settings.RADIO_UDP_ADDR(udp_port),
            )
        return succ, err

    @classmethod
    def start_cmr_process(cls, ctx):
        """Start a CMR QProcess to automate CMR Operation"""

        if cls._cmr_proc is None:
            logger.info("Starting the CMR manager QProcess")

            # Needs to have this executable in the resources folder to run this.
            program = ctx.get_resource("cmr_manager/cmr_manager")
            args = [
                "--port",
                "{}".format(conn_settings.CMR_PORT),
                "--ip",
                "{}".format(conn_settings.IP),
            ]

            # starting the QProcess
            cls._cmr_proc = QProcess()
            cls._cmr_proc.setProcessChannelMode(QProcess.MergedChannels)
            cls._cmr_proc.setProcessEnvironment(QProcessEnvironment.systemEnvironment())
            cls._cmr_proc.readyRead.connect(
                lambda: print(
                    cls._cmr_proc.readAllStandardOutput().data().decode().strip()
                )
            )
            cls._cmr_proc.start(program, args)
            succ = cls._cmr_proc.waitForStarted()
            err = None

            if not succ:
                err = "Failed to start CMR process"
                logger.info(err)
        else:
            succ = False
            err = "CMR Process already running"

        return succ, err

    @classmethod
    def stop_cmr_process(cls):
        """Stops the CMR QProcess."""

        if "windows" in platform.system().lower():
            cls._cmr_proc.kill()
        else:
            cls._cmr_proc.terminate()
            time.sleep(0.125)
        cls._cmr_proc = None

        succ = True
        err = ""
        return succ, err

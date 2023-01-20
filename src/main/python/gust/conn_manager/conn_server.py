import json
import platform
import logging
import time, sys
import random
from time import sleep

from PyQt5.QtCore import QProcess, QProcessEnvironment
from PyQt5 import QtNetwork

from utilities import ConnSettings as conn_settings
import utilities.database as database
from utilities import send_info_to_udp_server


logger = logging.getLogger(__name__)
logger.propagate = False


class ConnServer:
    running = False
    _radios = {}
    available_udp_ports = []
    _radio_udp_port = {}
    _cmr_proc = None
    _zeds = None
    _debug = False

    @classmethod
    def start_conn_server(cls, process_events, debug, ctx):
        """UDP Socket Server.

        Allow the connection server to start listening to socket connection and
        send each connection to other modules based on received message type

        Receives dictionary from the client sockets and sends back dictionary.
        One of the keys in the dictionary is 'type'
        """
        cls._debug = debug
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

        if cls.running:
            logger.warning("Already running!!")
            return

        cls.running = True

        cls.available_udp_ports = conn_settings.RADIO_PORTS

        conn = QtNetwork.QUdpSocket()
        conn.bind(conn_settings.PORT)

        msg = "Listening at {}:{}".format(conn_settings.IP, conn_settings.PORT)
        logger.info(msg)

        if not database.connect_db():
            cls.running = False
            logger.critical("Failed to connect to database, stopping conn_server")

        while cls.running:
            process_events()

            # Receiving message from client socket
            if not conn.hasPendingDatagrams():
                continue

            data = conn.receiveDatagram(conn.pendingDatagramSize())
            received_info = json.loads(data.data().data().decode(conn_settings.FORMAT))
            addr = data.senderAddress()
            port = data.senderPort()
            msg = "Message from {} -> {}".format(
                addr.toString().split(":")[-1], received_info
            )
            logger.info(msg)
            if received_info["type"] == conn_settings.DRONE_CONN:
                succ, err = cls.connect_to_radio(received_info, ctx)
                response = {"success": succ, "info": err}

            elif received_info["type"] == conn_settings.DRONE_DISC:
                name = received_info["name"]
                if name in cls._radios:
                    if "windows" in platform.system().lower():
                        cls._radios[name].kill()
                    else:
                        cls._radios[name].terminate()
                        time.sleep(0.125)
                    del cls._radios[name]
                    database.change_connection_status_value(name, 0)
                    response = {"success": True, "info": ""}
                else:
                    response = {
                        "success": False,
                        "info": "Radio connection not found in conn_server",
                    }

            elif received_info["type"] == conn_settings.ZED_CONN:
                succ, err = cls.connect_to_zed(received_info, ctx)
                response = {"success": succ, "info": err}

            elif received_info["type"] == conn_settings.ZED_DIS_CONN:
                succ, err = cls.disconnect_zed(received_info)
                response = {"success": succ, "info": err}

            elif received_info["type"] == conn_settings.AUTO_CMD:
                succ, err = cls.send_autopilot_commands(received_info)
                response = {"success": succ, "info": err}

            elif received_info["type"] == conn_settings.UPLOAD_WP:
                wp_color = received_info['wp_color']
                filename = ctx.get_resource('cmr_planning/{}_waypoints.txt'.format(wp_color))
                received_info[filename] = filename
                succ, err = cls.send_autopilot_commands(received_info)
                response = {"success": succ, "info": err}

            elif received_info["type"] == conn_settings.GOTO_NEXT_WP:
                succ, err = cls.send_autopilot_commands(received_info)
                response = {"success": succ, "info": err}

            elif received_info["type"] == conn_settings.START_CMR:
                succ, err = cls.start_cmr_process(ctx)
                response = {"success": succ, "info": err}

            elif received_info["type"] == conn_settings.STOP_CMR:
                succ, err = cls.stop_cmr_process()
                resposne = {"success": succ, "info": err}

            else:
                response = {
                    "success": False,
                    "info": "Signal not recognized by conn_server. \n Received signal: {}".format(
                        str(received_info)
                    ),
                }


            # Sending message back to client socket
            f_response = json.dumps(response).encode(conn_settings.FORMAT)
            conn.writeDatagram(f_response, addr, port)

        logger.info("Closing the conn-server socket")
        # conn.shutdown()
        conn.close()

    @classmethod
    def kill(cls):
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

        # killing the radio manager process
        for k, p in cls._radios.items():
            if "windows" in platform.system().lower():
                p.kill()
            else:
                p.terminate()
            if not p.waitForFinished():
                logger.critical("Failed to end radio process: %s", k)

    @classmethod
    def connect_to_zed(cls, received_info, ctx):
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
        name = received_info["name"]
        cls._radio_udp_port[name] = random.choice(cls.available_udp_ports)
        msg = "Connecting to {} on {}: udp connection: {}".format(
            name, received_info["port"], cls._radio_udp_port[name]
        )
        logger.info(msg)

        program = ctx.get_resource("radio_manager/radio_manager")
        args = [
            "--name",
            "{}".format(name),
            "--port",
            "{}".format(received_info["port"]),
            "--color",
            "{}".format(received_info["color"]),
            "--baud",
            "{}".format(received_info["baud"]),
            "--udp_port",
            "{}".format(cls._radio_udp_port[name]),
        ]

        if name in cls._radios:
            succ = False
            err = "Radio process already running"

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
                logger.info(err)
                return succ, err

            err = None
            cls.available_udp_ports.remove(cls._radio_udp_port[name])
        return succ, err

    @classmethod
    def send_autopilot_commands(cls, received_info):
        name = received_info["name"]
        udp_port = cls._radio_udp_port[name]
        succ, err = send_info_to_udp_server(
            received_info, received_info["type"], conn_settings.RADIO_UDP_ADDR(udp_port)
        )
        return succ, err

    @classmethod
    def upload_waypoints(cls, received_info):
        name = received_info["name"]
        udp_port = cls._radio_udp_port[name]
        succ, err = send_info_to_udp_server(
            received_info,
            conn_settings.UPLOAD_WP,
            conn_settings.RADIO_UDP_ADDR(udp_port),
        )
        return succ, err

    @classmethod
    def goto_next_waypoint(cls, received_info):
        name = received_info["name"]
        udp_port = cls._radio_udp_port[name]
        succ, err = send_info_to_udp_server(
            received_info,
            conn_settings.GOTO_NEXT_WP,
            conn_settings.RADIO_UDP_ADDR(udp_port),
        )
        logger.info(
            "This is what is received from the radio_manager-->> {}".format(err)
        )
        return succ, err

    @classmethod
    def start_cmr_process(cls, ctx):
        if cls._cmr_proc is None:
            logger.info("Starting the CMR manager QProcess")
            program = ctx.get_resource("cmr_manager/cmr_manager")
            args = [
                "--port",
                "{}".format(conn_settings.CMR_PORT),
                "--ip",
                "{}".format(conn_settings.IP),
            ]

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
        if "windows" in platform.system().lower():
            cls._cmr_proc.kill()
        else:
            cls._cmr_proc.terminate()
            time.sleep(0.125)
        cls._cmr_proc = None

        succ = True
        err = ""

        return succ, err

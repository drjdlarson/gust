#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 12:18:20 2022

@author: lagerprocessor
"""
import json
import platform
import logging
import time
from PyQt5.QtCore import QProcess, QProcessEnvironment
from PyQt5 import QtNetwork
from utilities import ConnSettings as conn_settings
import utilities.database as database
from gust.conn_manager.zed_handler import zedHandler


logger = logging.getLogger("[conn-server]")

class ConnServer:
    running = False
    _radios = {}
    _cmr_proc = None

    @classmethod
    def start_conn_server(cls, ctx):
        """UDP Socket Server.

        Allow the connection server to start listening to socket connection and
        send each connection to other modules based on received message type

        Receives dictionary from the client sockets and sends back dictionary.
        One of the keys in the dictionary is 'type'
        """
        if cls.running:
            logger.warning("Already running!!")
            return

        cls.running = True

        database.connect_db()
        conn = QtNetwork.QUdpSocket()
        conn.bind(conn_settings.PORT)

        msg = "Listening at {}:{}".format(conn_settings.IP, conn_settings.PORT)
        logger.info(msg)

        while cls.running:

            # Receiving message from client socket
            if not conn.hasPendingDatagrams():
                continue

            # data, addr = conn.recvfrom(conn_settings.MAX_MSG_SIZE)
            # received_info = json.loads(data.decode(conn_settings.FORMAT))
            data = conn.receiveDatagram(conn.pendingDatagramSize())
            received_info = json.loads(data.data().data().decode(conn_settings.FORMAT))
            addr = data.senderAddress()
            port = data.senderPort()
            msg = "Message from {} -> {}".format(addr.toString().split(":")[-1], received_info)
            logger.info(msg)

            # we can call the radio manager heres
            if received_info['type'] == conn_settings.DRONE_CONN:
                succ, err = cls.connect_to_radio(received_info, ctx)
                response = {'success': succ, 'info': err}

            elif received_info['type'] == conn_settings.DRONE_DISC:
                name = received_info['name']
                if name in cls._radios:
                    if 'windows' in platform.system().lower():
                        cls._radios[name].kill()
                    else:
                        cls._radios[name].terminate()
                        time.sleep(0.125)
                    del cls._radios[name]
                    database.change_connection_status_value(name, 0)

            elif received_info['type'] == conn_settings.ZED_CONN:
                response = zedHandler.connect(received_info)

            elif received_info['type'] == conn_settings.UPLOAD_WP:
                succ, err = cls.upload_waypoints(received_info)
                response = {'success': succ, 'info': err}

            elif received_info['type'] == conn_settings.START_CMR:
                succ, err = cls.start_cmr_process(ctx)
                response = {'success': succ, 'info': err}

            elif received_info['type'] == conn_settings.STOP_CMR:
                succ, err = cls.stop_cmr_process()
                resposne = {'success': succ, 'info': err}

            else:
                continue

            # Sending message back to client socket
            f_response = json.dumps(response).encode(conn_settings.FORMAT)
            # conn.sendto(f_response, addr)
            conn.writeDatagram(f_response, addr, port)

        logger.info("Closing the conn-server socket")
        # conn.shutdown()
        conn.close()

    @classmethod
    def kill(cls):
        zedHandler.kill()
        cls.running = False
        for p in cls._radios.values():
            if 'windows' in platform.system().lower():
                p.kill()
            else:
                p.terminate()
                time.sleep(0.125)

    @classmethod
    def connect_to_radio(cls, received_info, ctx):
        name = received_info['name']
        msg = "Connecting to {} on {}".format(name, received_info['port'])
        logger.info(msg)

        program = ctx.get_resource('radio_manager/radio_manager')
        args = [
            '--name',
            "{}".format(name),
            "--port",
            "{}".format(received_info['port']),
            "--color",
            "{}".format(received_info['color']),
            "--baud",
            "{}".format(received_info['baud']),
            ]

        if name in cls._radios:
            succ = False
            err = 'Radio process already running'

        else:
            cls._radios[name] = QProcess()
            cls._radios[name].setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
            cls._radios[name].setProcessEnvironment(QProcessEnvironment.systemEnvironment())
            cls._radios[name].start(program, args)

            succ = cls._radios[name].waitForStarted()
            if not succ:
                logger.info("Failed to start Radio process")
            err = None

        return succ, err

    @classmethod
    def upload_waypoints(cls, received_info):
        succ = False
        err = "There's nothing here right now, but its working"
        return succ, err

    @classmethod
    def start_cmr_process(cls, ctx):
        if cls._cmr_proc is None:
            logger.info("Starting the CMR manager QProcess")
            program = ctx.get_resource('cmr_manager/cmr_manager')
            args = []

            cls._cmr_proc = QProcess()
            cls._cmr_proc.setProcessChannelMode(QProcess.MergedChannels)
            cls._cmr_proc.setProcessEnvironment(QProcessEnvironment.systemEnvirotnment())
            cls._cmr_proc.start(program, args)

            succ = cls._cmr_proc.waitForStarted()
            err = None

            if not succ:
                err = 'Failed to start CMR process'
                logger.info(err)

        else:
            succ = False
            err = "CMR Process already running"

        return succ, err

    @classmethod
    def stop_cmr_process(cls):
        if 'windows' in platform.system().lower():
            cls._cmr_proc.kill()
        else:
            cls._cmr_proc.terminate()
            time.sleep(0.125)
        cls._cmr_proc = None

        succ = True
        err = ""

        return succ, err


# if __name__ == "__main__":
#     start_conn_server()
#     print("Starting the conn_server ...")

#     empty = {}
#     empty.update({'type': conn_settings.DRONE_CONN})
#     print(empty['type'])
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 12:18:20 2022

@author: lagerprocessor
"""
import json
import logging

from PyQt5 import QtNetwork

import gust.conn_manager.conn_settings as conn_settings
from gust.conn_manager.radio_manager import radioManager
from gust.conn_manager.zed_handler import zedHandler


logger = logging.getLogger("[conn-server]")


class ConnServer:
    running = False

    @classmethod
    def start_conn_server(cls):
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
            msg = "Message from {} -> {}".format(addr.toString(), received_info)
            logger.info(msg)

            # we can call the radio manager heres
            if received_info['type'] == conn_settings.DRONE_CONN:
                response = radioManager.connect_to_radio(received_info)
                # logger.debug(response)

            elif received_info['type'] == conn_settings.DRONE_DISC:
                response = radioManager.disconnect_radio(received_info)

            elif received_info['type'] == conn_settings.ZED_CONN:
                response = zedHandler.connect(received_info)

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



# if __name__ == "__main__":
#     start_conn_server()
#     print("Starting the conn_server ...")

#     empty = {}
#     empty.update({'type': conn_settings.DRONE_CONN})
#     print(empty['type'])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 12:18:20 2022

@author: lagerprocessor
"""
import json
import socket
import logging
import gust.conn_manager.conn_settings as conn_settings
from gust.conn_manager.radio_manager import radioManager


logger = logging.getLogger("[conn-server]")

# TODO: 1. figure out closing of conn_server appropriately
#           (parent.stop_conn_server gets bool from backend to stop,
#            I can't figure out how to use that to stop the while loop)
#       2. add other if then statements for proper connection routing


def start_conn_server(parent):
    """
    UDP Socket Server

        Allow the connection server to start listening to socket connection and
        send each connection to other modules based on received message type

        Receives dictionary from the client sockets and sends back dictionary.
        One of the keys in the dictionary is 'type'


    Returns
    -------
    None.

    """

    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.bind(conn_settings.ADDR())

    msg = "Listening at {}:{}".format(conn_settings.IP, conn_settings.PORT)
    logger.info(msg)


    while True:

        # Receiving message from client socket
        data, addr = conn.recvfrom(conn_settings.MAX_MSG_SIZE)
        received_info = json.loads(data.decode(conn_settings.FORMAT))
        msg = "Message from {} -> {}".format(addr, received_info)
        logger.info(msg)

        # we can call the radio manager here
        if received_info['type'] == conn_settings.DRONE_CONN:
            response = radioManager.connect_to_radio(received_info)
            response = {"success": True, "info": ""}

        elif received_info['type'] == conn_settings.DRONE_DISC:
            response = radioManager.disconnect_radio(received_info)

        # Sending message back to client socket
        # response = {"success": True, 'info': ''}
        f_response = json.dumps(response).encode(conn_settings.FORMAT)
        conn.sendto(f_response, addr)

        # if parent.stop_conn_server:
        #     logger.info("parent.stop_conn_server:: {}".format(parent.stop_conn_server))
        #     break

    logger.info("closing the conn-server socket")
    # conn.shutdown()
    conn.close()



if __name__ == "__main__":
    start_conn_server()
    print("Starting the conn_server ...")

    empty = {}
    empty.update({'type': conn_settings.DRONE_CONN})
    print(empty['type'])

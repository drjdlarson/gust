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


logger = logging.getLogger("[conn-server]")
conn_server_running = False

# TODO: 1. figure out closing of conn_server appropriately
#       2. add other if then statements for proper connection routing


def start_conn_server():
    """
    UDP Socket Server

        Allow the connection server to start listening to socket connection and
        send each connection to other modules based on received message type

        Receives dictionary from the client sockets and sends back dictionary.
        One of the keys in the dictionary is 'type'

        Message will be routed to specific point depending on the message type

    Returns
    -------
    None.

    """
    global conn_server_running
    if conn_server_running:
        msg = "Conn-server is already running"
        logger.warning(msg)

    else:
        conn_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        conn_server.bind(conn_settings.ADDR())

        msg = "Listening at {}:{}".format(conn_settings.IP, conn_settings.PORT)
        logger.info(msg)

        while True:

            # Receiving message from client socket
            data, addr = conn_server.recvfrom(conn_settings.MAX_MSG_SIZE)
            msg = json.loads(data.decode(conn_settings.FORMAT))

            # we can call the radio manager here
            msg = "Message from {} -> {}".format(addr, msg)
            logger.info(msg)

            # Sending message back to client socket
            response = {"success": True, 'info': ''}
            f_response = json.dumps(response).encode(conn_settings.FORMAT)
            conn_server.sendto(f_response, addr)


if __name__ == "__main__":
    start_conn_server()
    print("Starting the conn_server ...")

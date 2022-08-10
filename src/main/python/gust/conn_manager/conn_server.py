#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 12:18:20 2022

@author: lagerprocessor
"""
import json
import socket
import threading
import logging
import gust.conn_manager.conn_settings as conn_settings
import gust.database as database
import time
import random

conn_server_running = False
logger = logging.getLogger("[conn_server]")


def handle_connection(conn, addr):
    """Each thread of this function will handle individual connection between client and server"""

    msg = "{} connected to conn_server".format(addr)
    logger.info(msg)
    print(msg)

    connected = True
    while connected:
        msg_length = conn.recv(conn_settings.HEADER).decode(conn_settings.FORMAT)

        if msg_length:
            msg_length = int(msg_length)

            msg = conn.recv(msg_length).decode(conn_settings.FORMAT)
            msg = json.loads(msg)

            if msg == conn_settings.DISC_MSG:
                connected = False
                print("the client has disconnected")

            fmsg = "message from {} -->> {}".format(addr, msg)
            logger.info(fmsg)
            print(fmsg)

            if isinstance(msg, dict):
                print("the above message is a dictionary")
                res = manage_radio_conn(msg)

            # sending message back to the client
            conn.send("Message received at conn_server".encode(conn_settings.FORMAT))
    conn.close()


def start_conn_server():
    """Allow the connection server to start listening to connections,
        and pass each connection to handle_connection as a thread"""

    global conn_server_running
    if conn_server_running:
        msg = "Conn_server is already running"
        print(msg)
        logger.warning(msg)

    else:
        conn_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_server.bind(conn_settings.ADDR)
        conn_server.listen(conn_settings.MAX_CONNECTIONS)

        msg = "Listening on {}:{}".format(conn_settings.IP, conn_settings.PORT)
        logger.info(msg)
        print(msg)
        conn_server_running = True

        while True:
            conn, addr = conn_server.accept()
            thread = threading.Thread(target=handle_connection, args=(conn, addr))
            thread.start()

            msg = "New Connection: Active Connection count: {}".format(
                threading.activeCount() - 1
            )
            logger.info(msg)
            print(msg)




def manage_radio_conn(vehicle_info):
    name = vehicle_info['name']
    port = vehicle_info['port']

    database.open_db()
    res = database.add_vehicle(name, port)

    # if port == '/dev/test':
        # poll_dummy_radio(name)

    return res


def poll_dummy_radio(name):
    # while True:
    for _ in range(0, 20):
        write_dummy_into_database(name)
        time.sleep(0.5)

def write_dummy_into_database(name):
    randf1 = round(random.uniform(50, 100), 2)
    randf11 = round(random.uniform(0, 20), 2)
    randf111 = round(random.uniform(-60, 60), 2)
    randint1 = random.randint(0, 1)
    gnss_fix1 = random.randint(0, 2)
    mode1 = random.randint(0, 3)

    rate2 = {
        "rate": database.DroneRates.RATE2,
        "vals": {
            "m_time": randf1,
            "roll_angle": randf11,
            "pitch_angle": randf11,
            "heading": randf1,
            "track": randf1,
            "vspeed": randf1,
            "gndspeed": randf1,
            "airspeed": randf1,
            "latitude": randf111,
            "longitude": randf111,
            "altitude": randf1,
        },
    }
    rate1 = {
        "rate": database.DroneRates.RATE1,
        "vals": {
            "m_time": randf1,
            "flt_mode": mode1,
            "arm": randint1,
            "gnss_fix": gnss_fix1,
            "voltage": randf1,
            "current": randf1,
            "next_wp": randint1 + 12,
            "tof": randf1,
            " relay_sw": randint1,
            "engine_sw": randint1,
            "connection": 1,
        },
    }
    all_data = [rate1, rate2]
    database.write_values(all_data, name)


def test_func():
    for i in range(0, 100):
        time.sleep(0.001)
        msg = "testing function in line {}".format(i)
        logger.info(msg)
        print(msg)


if __name__ == "__main__":
    start_conn_server()
    print("Starting the conn_server ...")

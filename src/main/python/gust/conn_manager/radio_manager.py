#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 17:42:29 2022

@author: lagerprocessor
"""
import random
import time
import logging
from gust.worker import Worker
import gust.database as database
from time import sleep
from PyQt5.QtCore import QThreadPool, QTimer, pyqtSlot, pyqtSignal, QObject

logger = logging.getLogger("[radio-manager]")


class RadioManager(QObject):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.conn_status = {}
        self.debug = False

    def connect_to_radio(self, info):
        name = info["name"]
        port = info["port"]
        msg = "Connecting to {} on {}".format(name, port)
        logger.info(msg)

        # creating separate threads for each connection
        self.conn_status.update({name: True})
        worker = Worker(self.poll_radio, name, port)
        self.threadpool.start(worker)
        # return {"success": True, 'info': ''}

    def disconnect_radio(self, info):
        logger.debug("msg received for disconnection -->> {}".format(info))
        name = info['name']
        self.conn_status.update({name: False})
        res = database.change_connection_status_value(name, 0)
        if res:
            return {"success": True, "info": ""}


    def poll_radio(self, name, port):
        # for testing purposes only
        if port == "/dev/test/":
            msg = "Populating database with dummy data..."
            logger.info(msg)

            while self.conn_status[name]:
                self.write_dummy_into_database(name)
                time.sleep(0.5)

        else:
            msg = "Hardware needs to be configured"
            logger.warning(msg)


    def write_dummy_into_database(self, name):
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
        res = database.write_values(all_data, name)


radioManager = RadioManager()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 17:42:29 2022

@author: lagerprocessor
"""
import random
from gust.worker import Worker
import gust.database as database
from time import sleep
from PyQt5.QtCore import QThreadPool, QTimer, pyqtSlot, pyqtSignal, QObject


class RadioManager(QObject):

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.debug = False

    def connect_to_radio(self, name, port):
        print("Connecting to radio..")

        # for testing purposes only
        if port == '/dev/test':
            print("name is {} and port is {}".format(name, port), flush=True)

            worker = Worker(self.poll_dummy_radio, name)
            self.threadpool.start(worker)
            print("self.debug is {}".format(self.debug))
            return True

    def poll_radio(self, port):
        pass

    def dummy_connection(self, port):
        """No Action required to connect to dummy port"""
        print("dummy port {} is being connected".format(port), flush=True)
        return True

    # @pyqtSlot()
    def poll_dummy_radio(self, name):
        # create dummy value and write into database
        print("Poll dummy radio is active", flush=True)

        while True:
            self.write_dummy_into_database(name)
            sleep(0.5)


    @pyqtSlot()
    def write_dummy_into_database(self, name):
        randf1 = round(random.uniform(50, 100), 2)
        randf11 = round(random.uniform(0, 20), 2)
        randf111 = round(random.uniform(-60, 60), 2)
        randint1 = random.randint(0, 1)
        gnss_fix1 = random.randint(0, 2)
        mode1 = random.randint(0, 3)

        rate2 = {'rate': database.DroneRates.RATE2, 'vals': {'m_time': randf1, 'roll_angle': randf11, 'pitch_angle': randf11, 'heading': randf1, 'track': randf1, 'vspeed': randf1, 'gndspeed': randf1, 'airspeed': randf1, 'latitude': randf111, 'longitude': randf111, 'altitude': randf1}}
        rate1 = {'rate': database.DroneRates.RATE1, 'vals': {'m_time': randf1, 'flt_mode': mode1, 'arm': randint1, 'gnss_fix': gnss_fix1, 'voltage': randf1, 'current': randf1, 'next_wp': randint1 + 12, 'tof': randf1, ' relay_sw': randint1, 'engine_sw': randint1, 'connection': 1}}

        all_data = [rate1, rate2]
        database.write_values(all_data, name)


@pyqtSlot()
def poll_dummy_radio():
    # create dummy value and write into database
    print("poll dummy radio function is here", flush=True)

radioManager = RadioManager()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 17:42:29 2022

@author: lagerprocessor
"""
import random
import time
from queue import Queue
from gust.worker import Worker
import gust.database as database
from time import sleep
from PyQt5.QtCore import QThreadPool, QTimer, pyqtSlot, pyqtSignal, QObject

from queue import Queue
import threading


class RadioManager(QObject):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.debug = False
        self.q = Queue()

        self.connected = []
        self.threadlist = []

    def connect_to_radio(self, name, port):
        print("Connecting to radio..")

        # for testing purposes only
        if port == "/dev/test":
            print("name is {} and port is {}".format(name, port), flush=True)

            self.connected.append(name)

            self.q.put(name)
            worker = Worker(self.worker)
            self.threadpool.start(worker)

            # self.q.put(name)
            # thread = threading.Thread(target=self.worker)
            # self.threadlist.append(thread)
            # thread.start()


            # for t in self.connected:
            #     thread = threading.Thread(target=self.worker)
            #     self.threadlist.append(thread)
            # for thread in self.threadlist:
            #     if not thread.is_alive():
            #         thread.start()
            # for thread in self.threadlist:
            #     thread.join()



    def error_msg(self):
        print("SOME ERROR")

    def showing_result(self, s):
        print("result is {}".format(s))

    def thread_complete(self):
        print("Thread Complete")
        self.conn_status = True

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

        # while True:
        #     self.write_dummy_into_database(name)
        #     sleep(0.5)


    def worker(self):
        print("in the worker section")
        while not self.q.empty():
            name = self.q.get()
            while True:
                self.write_dummy_into_database(name)
                time.sleep(0.5)


    @pyqtSlot()
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
        database.write_values(all_data, name)


radioManager = RadioManager()

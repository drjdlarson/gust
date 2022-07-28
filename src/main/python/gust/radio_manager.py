#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 17:42:29 2022

@author: lagerprocessor
"""
from gust.worker import Worker
import gust.database as database
from PyQt5.QtCore import QThreadPool, QTimer


class RadioManager():

    def __init__(self):
        # self.threadpool = QThreadPool()
        pass

    def pull_radio(self, port):
        pass


    def connect_to_radio(self, name, port):
        print("Connecting to radio..")
        if port == '/dev/test':
            print("name is {} and port is {}".format(name, port))
            # worker = Worker(self.pull_dummy_radio, port)
            # self.threadpool.start(worker)
        return False


    def pull_dummy_radio(self, port):
        # create dummy value and write into database
        pass


# if self.timer is None:
#     self.timer = QTimer()
#     self.timer.timeout.connect(self.write_into_database)
#     self.timer.start(66)

# @pyqtSlot()
# def pass_dummy_data(self):
#     """Writes the set of flight data into database"""
#     import gust.database as database
#     from gust.database import DroneRates

#     # generating random numbers
#     randf1 = round(random.uniform(50, 100), 2)
#     randf11 = round(random.uniform(0, 20), 2)
#     randf111 = round(random.uniform(-60, 60), 2)
#     randint1 = random.randint(0, 1)
#     gnss_fix1 = random.randint(0, 2)
#     mode1 = random.randint(0, 3)

#     randf2 = round(random.uniform(50, 100), 2)
#     randf22 = round(random.uniform(0, 20), 2)
#     randf222 = round(random.uniform(-60, 60), 2)
#     randint2 = random.randint(0, 1)
#     gnss_fix2 = random.randint(0, 2)
#     mode2 = random.randint(0, 3)

#     rate2 = {'rate': DroneRates.RATE2, 1: {'m_time': randf1, 'roll_angle': randf11, 'pitch_angle': randf11, 'heading': randf1, 'track': randf1, 'vspeed': randf1, 'gndspeed': randf1, 'airspeed': randf1, 'latitude': randf111, 'longitude': randf111, 'altitude': randf1},
#              2: {'m_time': randf2, 'roll_angle': randf22, 'pitch_angle': randf22, 'heading': randf2, 'track': randf2, 'vspeed': randf2, 'gndspeed': randf2, 'airspeed': randf2, 'latitude': randf222, 'longitude': randf222, 'altitude': randf2}}

#     rate1 = {'rate': DroneRates.RATE1, 1: {'m_time': randf1, 'flt_mode': mode1, 'arm': randint1, 'gnss_fix': gnss_fix1, 'voltage': randf1, 'current': randf1, 'next_wp': randint1 + 12, 'tof': randf1, ' relay_sw': randint1, 'engine_sw': randint1, 'connection': randint1},
#              2: {'m_time': randf2, 'flt_mode': mode2, 'arm': randint2, 'gnss_fix': gnss_fix2, 'voltage': randf2, 'current': randf2, 'next_wp': randint2 + 15, 'tof': randf2, ' relay_sw': randint2, 'engine_sw': randint2, 'connection': randint2}}

#     all_data = [rate1, rate2]
#     database.write_values(all_data)

# @pyqtSlot()
# def write_into_database(self):
#     # continously write data into the database on the server has been started

#     # msg = '-------writing into database-------\n'
#     # self.update_console_text(msg)
#     return

# # @pyqtSlot(dict)
# # def add_drone(self, passed_info):

# #     self.update_console_text("we are in the add drone section")

# #     import gust.database as database
# #     from gust.database import DroneRates

# #     name = passed_info['name']
# #     port = passed_info['port']

# #     communicator.conn_info_res = True
# #     self.update_console_text('on the add drone section')
# #     self.update_console_text("name {}, port {}".format(name, port))

#     # connected_vehicles = database.get_drone_ids(True)

#     # # checking if the drone we're trying to connect already exists in database
#     if name not in connected_vehicles:

#         # For Testing purpose only
#         if port == '/dev/test':
#             res1 = database.add_vehicle(name)
#             return res1

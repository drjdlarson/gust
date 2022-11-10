#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 17:42:29 2022

@author: lagerprocessor
"""
import numpy as np
import random
import time
import logging
from gust.worker import Worker
import utilities.database as database
import math
import dronekit
from PyQt5.QtCore import QThreadPool, QTimer, pyqtSlot, pyqtSignal, QObject

logger = logging.getLogger("[radio-manager]")

d2r = np.pi / 180
r2d = 1 / d2r


# TODO: manage data properly in prepare_data_from_mavlink() before writing in database.
# make sure the datatypes are correct. current is TEXT when "NONE", but INT when not "NONE"

class RadioManager(QObject):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.debug = False
        self.conn = {}

    def connect_to_radio(self, info):
        name = info["name"]
        port = info["port"]
        color = info["color"]
        baud = info["baud"]
        msg = "Connecting to {} on {}".format(name, port)
        logger.info(msg)
        self.conn[name] = {}
        self.conn[name]['type'] = 'TEST_PORT'

        if port != "/dev/test/":
            self.conn[name]['type'] = 'HARDWARE'
            if baud < 0:
                return {"success": False, "info": "Invalid baud rate {}".format(baud)}
            try:
                logger.info("Initiating mavlink connection")
                self.conn[name]['conn'] = dronekit.connect(port, wait_ready=True, baud=baud)
                # self.radios[name] = dronekit.connect(port, wait_ready=True, baud=baud)
            except:
                return {"success": False, "info": "Unable to connect to radio"}

        # creating separate threads for each connection
        self.conn[name]['status'] = True
        worker = Worker(self.poll_radio, name, port)
        self.threadpool.start(worker)
        return {"success": True, "info": ''}

    def disconnect_radio(self, info):
        logger.debug("Disconnection Message: {}".format(info))
        name = info['name']

        if self.conn[name]['type'] == 'HARDWARE':
            # disconnecting mavlink connection
            self.conn[name]['conn'].close()

        self.conn[name]['status'] = False

        # chaning connection status on database
        res = database.change_connection_status_value(name, 0)
        if res:
            return {"success": True, "info": ""}

    def poll_radio(self, name, port):
        # for testing purposes only
        if port == "/dev/test/":
            msg = "Populating database with dummy data..."
            logger.info(msg)
            while self.conn[name]['status']:
                all_data = self.prepare_dummy_data()
                res = database.write_values(all_data, name)
                time.sleep(0.2)

        else:
            logger.info("Mavlink connection successfull")
            mav_data = {}

            # Setting the first set of data to be all zero
            all_data = self.prepare_dummy_data()
            res = database.write_values(all_data, name)

            rate1, rate2, rate3, rate4 = [all_data[i] for i in range(len(all_data))]
            while self.conn[name]['status']:
                rate1, rate2, rate3, rate4, mav_data = self.prepare_data_from_mavlink(
                    name, port, rate1, rate2, rate3, rate4, mav_data
                    )
                all_data = rate1, rate2, rate3, rate4
                res = database.write_values(all_data, name)
                time.sleep(0.1)


    def prepare_dummy_data(self):
        current_time = self.get_current_time()
        randf1 = round(random.uniform(50, 100), 2)
        randf11 = round(random.uniform(0, 20), 2)
        randf111 = round(random.uniform(-60, 60), 2)
        randf2 = random.uniform(-0.02, 0.02)
        randf22 = round(random.uniform(0, 1000))
        randf222 = round(random.uniform(0, 10))
        randf3 = random.uniform(-5, 5)
        randint1 = random.randint(0, 1)
        gnss_fix1 = random.randint(0, 2)
        mode1 = random.randint(0, 3)

        rate1 = {
            "rate": database.DroneRates.RATE1,
            "vals": {
                "m_time": current_time,
                "home_lat": 33.21534,
                "home_lon": -87.54355,
                "home_alt": 170,
                "voltage": randf1,
                "current": randf1,
            },
        }
        rate2 = {
            "rate": database.DroneRates.RATE2,
            "vals": {
                "m_time": current_time,
                "latitude": 33.21534 + randf2,
                "longitude": -87.54355 + randf2,
                "relative_alt": randf1,
                "yaw": randf22,
                "heading": randf22 + 20,
                "gnss_fix": mode1,
                "satellites_visible": randf11,
                "roll_angle": randf11,
                "pitch_angle": randf11,
                "alpha": randf3,
                "beta": randf3,
                "airspeed": randf1,
                "gndspeed": randf1,
                "vspeed": randf111,
                "throttle": randf1,
            },
        }
        rate3 = {
            "rate": database.DroneRates.RATE3,
            "vals": {
                "m_time": current_time,
                "chancount": randf11,
                "chan1_raw": randf22,
                "chan2_raw": randf22,
                "chan3_raw": randf22,
                "chan4_raw": randf22,
                "chan5_raw": randf22,
                "chan6_raw": randf22,
                "chan7_raw": randf22,
                "chan8_raw": randf22,
                "chan9_raw": randf22,
                "chan10_raw": randf22,
                "chan11_raw": randf22,
                "chan12_raw": randf22,
                "chan13_raw": randf22,
                "chan14_raw": randf22,
                "chan16_raw": randf22,
                "chan17_raw": randf22,
                "chan18_raw": randf22,
                "rssi": randf1,
                "servo_port": randf222,
                "servo1_raw": randf22,
                "servo2_raw": randf22,
                "servo3_raw": randf22,
                "servo4_raw": randf22,
                "servo5_raw": randf22,
                "servo6_raw": randf22,
                "servo7_raw": randf22,
                "servo8_raw": randf22,
                "servo9_raw": randf22,
                "servo10_raw": randf22,
                "servo11_raw": randf22,
                "servo12_raw": randf22,
                "servo13_raw": randf22,
                "servo14_raw": randf22,
                "servo15_raw": randf22,
                "servo16_raw": randf22,
            },
        }
        rate4 = {
            "rate": database.DroneRates.RATE4,
            "vals": {
                "m_time": current_time,
                "armed": random.choice([0, 1]),
                "flight_mode": random.choice(['STABILIZE', 'GUIDED', 'AUTO', 'RTL']),
                "mav_type": 2,
                "autopilot": 1,
                "custom_mode": 0,
                "tof": randf222,
                "next_wp": randf222,
                "relay_sw": randint1,
                "engine_sw": randint1,
            },
        }
        all_data = rate1, rate2, rate3, rate4
        return all_data

    def prepare_data_from_mavlink(self, name, port, rate1, rate2, rate3, rate4, data):
        current_time = self.get_current_time()

        radio = self.conn[name]['conn']
        data['MAV'] = {}
        data['ATTITUDE'] = {}
        data['VFR_HUD'] = {}
        # data['HEARTBEAT'] = {}
        # data['HOME'] = {}
        data['LOCAL_POSITION_NED'] = {}
        data['GLOBAL_POSITION_INT'] = {}
        data['BATTERY_STATUS'] = {}
        data['GPS_RAW_INT'] = {}


        # populating data{} before writing rates for database
        data['MAV']['armed'] = int(radio.armed)
        data['MAV']['base_mode'] = radio.mode.name
        data['MAV']['flight_mode'] = radio.mode.name
        data['MAV']['mav_type'] = 0
        data['vehicle_type'] = radio._vehicle_type

        data['ATTITUDE']['roll'] = radio.attitude.roll * r2d
        data['ATTITUDE']['pitch'] = radio.attitude.pitch * r2d

        data['VFR_HUD']['yaw'] = radio.attitude.yaw * r2d
        data['VFR_HUD']['airspeed'] = radio.airspeed
        data['VFR_HUD']['groundspeed'] = radio.groundspeed

        data['GLOBAL_POSITION_INT']['lat'] = radio.location._lat
        data['GLOBAL_POSITION_INT']['lon'] = radio.location._lon
        data['GLOBAL_POSITION_INT']['relative_alt'] = radio.location._relative_alt

        data['LOCAL_POSITION_NED']['vx'] = radio._vx
        data['LOCAL_POSITION_NED']['vy'] = radio._vy
        data['LOCAL_POSITION_NED']['heading'] = radio.heading

        data['BATTERY_STATUS']['voltage'] = radio.battery.voltage
        data['BATTERY_STATUS']['current'] = radio.battery.current

        data['GPS_RAW_INT']['fix_type'] = radio._fix_type
        data['GPS_RAW_INT']['satellites_visible'] = radio._satellites_visible

        # putting zero for things confused from dronekit
        data['VFR_HUD']['climb'] = 0
        data['VFR_HUD']['throttle'] = 0

        # populating rate dictionaries from mavlink data
        for rate in (rate1, rate2, rate3, rate4):
            rate["vals"]["m_time"] = current_time

        # Put zero for things not available currently
        rate1["vals"]["home_lat"] = 0
        rate1["vals"]["home_lon"] = 0
        rate1["vals"]["home_alt"] = 0

        rate4["vals"]["tof"] = 0
        rate4["vals"]["next_wp"] = 0
        rate4["vals"]["relay_sw"] = 0
        rate4["vals"]["engine_sw"] = 0
        rate2['vals']['alpha'] =0
        rate2['vals']['beta'] = 0


        if "MAV" in data:
            rate4["vals"]["flight_mode"] = data["MAV"]["base_mode"]
            rate4["vals"]["mav_type"] = data["MAV"]["mav_type"]
            rate4["vals"]["armed"] = data["MAV"]["armed"]

        if "ATTITUDE" in data:
            rate2['vals']['roll_angle'] = data['ATTITUDE']['roll']
            rate2['vals']['pitch_angle'] = data['ATTITUDE']['pitch']

        if 'VFR_HUD' in data:
            rate2['vals']['airspeed'] = round(data['VFR_HUD']['airspeed'])
            rate2['vals']['gndspeed'] = round(data['VFR_HUD']['groundspeed'], 1)
            rate2['vals']['yaw'] = round(data['VFR_HUD']['yaw'])
            rate2['vals']['vspeed'] = round(data['VFR_HUD']['climb'], 1)
            rate2['vals']['throttle'] = round(data['VFR_HUD']['throttle'])

        if 'LOCAL_POSITION_NED' in data:
            vx = data['LOCAL_POSITION_NED']['vx']
            vy = data['LOCAL_POSITION_NED']['vy']
            # rate2['vals']['heading'] = round(math.degrees(math.atan2(vy, vx)))
            rate2['vals']['heading'] = 0

        if 'GLOBAL_POSITION_INT' in data:
            rate2['vals']['latitude'] = data['GLOBAL_POSITION_INT']['lat']
            rate2['vals']['longitude'] = data['GLOBAL_POSITION_INT']['lon']
            rate2['vals']['relative_alt'] = data['GLOBAL_POSITION_INT']['relative_alt']

        if 'BATTERY_STATUS' in data:
            rate1['vals']['voltage'] = data['BATTERY_STATUS']['voltage']
            # rate1['vals']['current'] = data['BATTERY_STATUS']['current']
            rate1['vals']['current'] = 0

        if 'GPS_RAW_INT' in data:
            rate2['vals']['gnss_fix'] = data['GPS_RAW_INT']['fix_type']
            rate2['vals']['satellites_visible'] = data['GPS_RAW_INT']['satellites_visible']
        return rate1, rate2, rate3, rate4, data


    def get_current_time(self):
        return time.time()

radioManager = RadioManager()

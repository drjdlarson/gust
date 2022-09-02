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
import math
from radio_receiver import RadioReceiver
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
        return {"success": True, "info": ''}

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
                all_data = self.prepare_dummy_data()
                res = database.write_values(all_data, name)
                time.sleep(0.2)

        else:
            mav_data = {}

            # Setting the first set of data to be all zero
            all_data = self.prepare_dummy_data()
            zeroed_data = []
            for rate in all_data:
                rate["vals"] = dict.fromkeys(rate["vals"], 0)
                zeroed_data.append(rate)
            res = database.write_values(zeroed_data, name)

            rate1, rate2, rate3, rate4 = [zeroed_data[i] for i in range(len(zeroed_data))]
            while self.conn_status[name]:
                rate1, rate2, rate3, rate4, mav_data = self.prepare_data_from_mavlink(
                    port, rate1, rate2, rate3, rate4, mav_data
                    )
                res = database.write_values(all_data, name)
                # time.sleep(0.1)


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
                "heading": randf22,
                "track": randf22 + 45,
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
                "armed": random.choice([3, 4, 9]),
                "flight_mode": random.choice([128, 0]) + random.choice([16, 8, 24]),
                "mav_type": 2,
                "autopilot": 1,
                "custom_mode": 0,
                "tof": randf222,
                "next_wp": randf222,
                "relay_sw": randint1,
                "engine_sw": randint1,
                "connection": 1,
            },
        }
        all_data = rate1, rate2, rate3, rate4
        return all_data

    def prepare_data_from_mavlink(self, port, rate1, rate2, rate3, rate4, data):
        current_time = self.get_current_time()
        try:
            radio = RadioReceiver(port)
            available_packets = radio.get_available_messages()

            # getting the MAV packet separately
            try:
                msg = radio.connection.messages['MAV']
                mav_packet = {'armed': msg.armed, 'base_mode': msg.base_mode, 'flight_mode': msg.flightmode, 'mav_type': msg.mav_type, 'vehicle_type': msg.vehicle_type}
                data['MAV'] = mav_packet
            except:
                pass

            # excluding the MAV packet
            for packet in available_packets[1:]:
                try:
                    succ, msg, time_since = radio.get_msg(packet)
                    if succ:
                        data[packet] = radio.msg_to_dict(msg)
                except:
                    pass
        except:
            logger.warning("Heartbeat not received")

        # populating rate dictionaries from mavlink data
        for rate in (rate1, rate2, rate3, rate4):
            rate["vals"]["m_time"] = current_time

        rate4["vals"]["connection"] = 1

        # Put zero for things not available currently
        rate4["vals"]["tof"] = 0
        rate4["vals"]["next_wp"] = 0
        rate4["vals"]["relay_sw"] = 0
        rate4["vals"]["engine_sw"] = 0
        rate2['vals']['alpha'] =0
        rate2['vals']['beta'] = 0

        if "MAV" in data:
            rate4["vals"]["flight_mode"] = data["MAV"]["base_mode"]
            rate4["vals"]["mav_type"] = data["MAV"]["mav_type"]

        if "HOME" in data:
            rate1["vals"]["home_lat"] = data["HOME"]["lat"] * 10 ** -7
            rate1["vals"]["home_lon"] = data["HOME"]["lon"] * 10 ** -7
            rate1["vals"]["home_alt"] = data["HOME"]["alt"] * 10 ** -7

        if "HEARTBEAT" in data:
            rate4["vals"]["armed"] = data["HEARTBEAT"]["system_status"]
            rate4["vals"]["autopilot"] = data["HEARTBEAT"]["autopilot"]
            rate4["vals"]["custom_mode"] = data["HEARTBEAT"]["custom_mode"]


        if "ATTITUDE" in data:
            rate2['vals']['roll_angle'] = round(math.degrees(data['ATTITUDE']['roll']))
            rate2['vals']['pitch_angle'] = round(math.degrees(data['ATTITUDE']['pitch']))

        if 'VFR_HUD' in data:
            rate2['vals']['airspeed'] = round(data['VFR_HUD']['airspeed'])
            rate2['vals']['gndspeed'] = round(data['VFR_HUD']['groundspeed'], 1)
            rate2['vals']['heading'] = round(data['VFR_HUD']['heading'])
            rate2['vals']['vspeed'] = round(data['VFR_HUD']['climb'], 1)
            rate2['vals']['throttle'] = round(data['VFR_HUD']['throttle'])

        if 'LOCAL_POSITION_NED' in data:
            vx = data['LOCAL_POSITION_NED']['vx']
            vy = data['LOCAL_POSITION_NED']['vy']
            rate2['vals']['track'] = round(math.degrees(math.atan2(vy, vx)))

        if 'GLOBAL_POSITION_INT' in data:
            rate2['vals']['latitude'] = data['GLOBAL_POSITION_INT']['lat'] * 10 ** -7
            rate2['vals']['longitude'] = data['GLOBAL_POSITION_INT']['lon'] * 10 ** -7
            rate2['vals']['relative_alt'] = data['GLOBAL_POSITION_INT']['relative_alt']

        if 'BATTERY_STATUS' in data:
            rate1['vals']['voltage'] = data['BATTERY_STATUS']['voltages'][0] * 10 ** -3
            rate1['vals']['current'] = data['BATTERY_STATUS']['current_battery']

        if 'GPS_RAW_INT' in data:
            rate2['vals']['gnss_fix'] = data['GPS_RAW_INT']['fix_type']
            rate2['vals']['satellites_visible'] = data['GPS_RAW_INT']['satellites_visible']

        return rate1, rate2, rate3, rate4, data


    def get_current_time(self):
        return time.time()

radioManager = RadioManager()

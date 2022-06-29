# !/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:02:36 2022

@author: lagerprocessor
"""

import sys
import os
import time
from datetime import timedelta
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5. QtWidgets import QMainWindow, QMessageBox, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex, pyqtSignal, QThreadPool, QThread, QTimer
from PyQt5.QtGui import QIntValidator, QTextCursor
import requests
from gust.gui.ui.gustClient import Ui_MainWindow_main
from gust.gui import con_window, confirmation_window, log_window, sensors_window
from gust.gui.ui.map_widget import MapWidget
from gust.gui.ui.attitude_ind_widget import pyG5AIWidget

URL_BASE = "http://localhost:8000/api/"

class FrontendWindow(QMainWindow, Ui_MainWindow_main):
    """Main interface for the frontend window."""

    def __init__(self, ctx):
        super().__init__()
        self.timer = None
        self.manager = DataManager()
        self.ctx = ctx
        self.setupUi(self)

        # Pushbuttons
        self.pushButton_addvehicle.clicked.connect(self.clicked_addvehicle)
        self.pushButton_engineOff.clicked.connect(self.clicked_engineOff)
        self.pushButton_RTL.clicked.connect(self.clicked_RTL)
        self.pushButton_disarm.clicked.connect(self.clicked_disarm)
        self.pushButton_sensors.clicked.connect(self.clicked_sensors)

        self.pushButton_update.clicked.connect(self.update_request)
        self.pushButton_default.clicked.connect(self.clicked_default)

        self._conWindow = None
        self._confirmationWindow = None
        self._sensorsWindow = None

        header = self.tableWidget.horizontalHeader()
        header.setMinimumSectionSize(120)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)



    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

    @pyqtSlot()
    def clicked_addvehicle(self):
        self._conWindow = con_window.ConWindow(
            self.ctx)
        self._conWindow.show()

        # adding a row in the table
        rowPos = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPos)

    @pyqtSlot()
    def clicked_engineOff(self):
        self._confirmationWindow = confirmation_window.ConfirmationWindow(
            self.ctx)
        self._confirmationWindow.show()

    @pyqtSlot()
    def clicked_RTL(self):
        self._confirmationWindow = confirmation_window.ConfirmationWindow(
            self.ctx)
        self._confirmationWindow.show()

    @pyqtSlot()
    def clicked_disarm(self):
        self._confirmationWindow = confirmation_window.ConfirmationWindow(
            self.ctx)
        self._confirmationWindow.show()

    @pyqtSlot()
    def clicked_sensors(self):
        self._sensorsWindow = sensors_window.SensorsWindow(
            self.ctx)
        self._sensorsWindow.show()


    def update_request(self):
        if self.timer is None:
            self.timer = QTimer()
            self.manager.timer = self.timer
            self.manager.rate = 200
            self.timer.timeout.connect(self.manager.run)
            self.manager.signal.connect(self.update_frame)
            self.timer.start(200)


    def update_frame(self, passed_list):

        self.name = passed_list[0]
        self.altitude = passed_list[1]
        self.vspeed = passed_list[2]
        self.airspeed = passed_list[3]
        self.gndspeed = passed_list[4]
        self.voltage = passed_list[5]
        self.current = passed_list[6]
        self.engine_sw = passed_list[7]
        self.relay_sw = passed_list[8]
        self.mode = passed_list[9]
        self.arm = passed_list[10]
        self.gnss_fix = passed_list[11]
        self.roll_angle = passed_list[12]
        self.pitch_angle = passed_list[13]
        self.heading = passed_list[14]
        self.next_wp = passed_list[15]
        self.tof_hms = passed_list[16]
        self.connection = passed_list[17]
        self.track = passed_list[18]
        self.latitude = passed_list[19]
        self.longitude = passed_list[20]

        # updating the lcd display
        self.label_seluav.setText(str(self.name))
        self.lcdNumber_altitude.display(self.altitude)
        self.lcdNumber_vspeed.display(self.vspeed)
        self.lcdNumber_airspeed.display(self.airspeed)
        self.lcdNumber_gndspeed.display(self.gndspeed)
        self.lcdNumber_voltage.display(self.voltage)
        self.lcdNumber_current.display(self.current)


        # self.update_table(self)
        rowPos = self.tableWidget.rowCount()
        rowPos -= 1
        item = QTableWidgetItem(self.name)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 0, item)
        item = QTableWidgetItem(str(self.mode))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 1, item)
        item = QTableWidgetItem("Waypoint " + str(self.next_wp))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 2, item)
        item = QTableWidgetItem(str(self.tof_hms))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 3, item)
        item = QTableWidgetItem(str(self.altitude) + " m")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 4, item)
        item = QTableWidgetItem(str(self.voltage) + " V")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 5, item)
        item = QTableWidgetItem(str(self.current) + " A")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 6, item)
        item = QTableWidgetItem(str(self.relay_sw))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 7, item)
        item = QTableWidgetItem(str(self.engine_sw))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 8, item)
        item = QTableWidgetItem(str(self.connection))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 9, item)


        self.widget_hud.roll_angle = self.roll_angle
        self.widget_hud.pitch_angle = self.pitch_angle
        self.widget_hud.gndspeed = self.gndspeed
        self.widget_hud.airspeed = self.airspeed
        self.widget_hud.altitude = self.altitude
        self.widget_hud.vspeed = self.vspeed
        self.widget_hud.heading = self.heading
        self.widget_hud.arm = self.arm
        self.widget_hud.gnss_fix = self.gnss_fix
        self.widget_hud.mode= self.mode
        self.widget_hud.repaint()

        self.widget_map.clear_drone_list()
        self.widget_map.add_drone(
            self.name,
            self.latitude,
            self.longitude,
            self.heading,
            self.track,
            self.mode,
            self.ctx)
        self.widget_map.update_map()

    def clicked_default(self):
        self.label_seluav.setText("Current Vehicle Name")
        self.lcdNumber_altitude.display(100)
        self.lcdNumber_vspeed.display(100)
        self.lcdNumber_airspeed.display(100)
        self.lcdNumber_gndspeed.display(100)
        self.lcdNumber_voltage.display(100)
        self.lcdNumber_current.display(100)

        self.tableWidget.clearContents()
        self.widget_map.clear_drone_list()


class DataManager(QtCore.QObject):

    signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.rate = None
        self.timer = None

    @pyqtSlot()
    def run(self):

        # selected drone name
        url = "{}seluav".format(URL_BASE)
        r = requests.get(url).json()
        self.name = r['VehicleName']

        # altitude
        url = "{}altitude".format(URL_BASE)
        r = requests.get(url).json()
        self.altitude = r['Altitude']

        # vspeed
        url = "{}vspeed".format(URL_BASE)
        r = requests.get(url).json()
        self.vspeed = r['Vspeed']

        # airspeed
        url = "{}airspeed".format(URL_BASE)
        r = requests.get(url).json()
        self.airspeed = r['Airspeed']

        # Ground Speed
        url = "{}gndspeed".format(URL_BASE)
        r = requests.get(url).json()
        self.gndspeed = r['Gndspeed']

        # Voltage
        url = "{}voltage".format(URL_BASE)
        r = requests.get(url).json()
        self.voltage = r['Voltage']

        # current
        url = "{}current".format(URL_BASE)
        r = requests.get(url).json()
        self.current = r['Current']

        # engine switch
        url = "{}engine_sw".format(URL_BASE)
        r = requests.get(url).json()
        self.engine_sw = r['Engine Status']

        # relay switch
        url = "{}relay_sw".format(URL_BASE)
        r = requests.get(url).json()
        self.relay_sw = r['Relay Status']

        # mode state
        url = "{}mode".format(URL_BASE)
        r = requests.get(url).json()
        self.mode = r['Mode']

        # arm state
        url = "{}arm".format(URL_BASE)
        r = requests.get(url).json()
        self.arm = r['Arm']

        # gnss fix
        url = "{}gnss_fix".format(URL_BASE)
        r = requests.get(url).json()
        self.gnss_fix = r['Gnss_fix']

        # roll angle
        url = "{}roll_angle".format(URL_BASE)
        r = requests.get(url).json()
        self.roll_angle = r['Roll_angle']

        # pitch angle
        url = "{}pitch_angle".format(URL_BASE)
        r = requests.get(url).json()
        self.pitch_angle = r['Pitch_angle']

        # heading
        url = "{}heading".format(URL_BASE)
        r = requests.get(url).json()
        self.heading = r['Heading']

        # next waypoint
        url = "{}next_wp".format(URL_BASE)
        r = requests.get(url).json()
        self.next_wp = r['Next_wp']

        # time of flight
        url = "{}tof".format(URL_BASE)
        r = requests.get(url).json()
        tof = r['Tof']
        self.tof_hms = timedelta(seconds=tof)

        # connection
        url = "{}connection".format(URL_BASE)
        r = requests.get(url).json()
        self.connection = r['Connection']

        # track
        url = "{}track".format(URL_BASE)
        r = requests.get(url).json()
        self.track = r['Track']

        # latitude
        url = "{}latitude".format(URL_BASE)
        r = requests.get(url).json()
        self.latitude = r['Latitude']

        # Longitude
        url = "{}longitude".format(URL_BASE)
        r = requests.get(url).json()
        print(r)

        self.longitude = r['Longitude']

        self.signal_list = [self.name,
                            self.altitude,
                            self.vspeed,
                            self.airspeed,
                            self.gndspeed,
                            self.voltage,
                            self.current,
                            self.engine_sw,
                            self.relay_sw,
                            self.mode,
                            self.arm,
                            self.gnss_fix,
                            self.roll_angle,
                            self.pitch_angle,
                            self.heading,
                            self.next_wp,
                            self.tof_hms,
                            self.connection,
                            self.track,
                            self.latitude,
                            self.longitude
                            ]

        self.signal.emit(self.signal_list)
        print("worker {}".format(self.signal_list[1]))
        self.timer.start(self.rate)

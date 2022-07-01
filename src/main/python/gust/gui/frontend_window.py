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
            self.manager.rate = 500
            self.timer.timeout.connect(self.manager.run)
            self.manager.signal.connect(self.update_frame)
            self.timer.start(500)



    # def find_row(self, row):
    #     self.lcdNumber_altitude.display(row)


    def update_frame(self, passed_signal):

        self.widget_map.clear_drone_list()

        # filling up the table
        for key in passed_signal:
            rowPos = int(key) - 1

            item = passed_signal[key]['name']
            item = QTableWidgetItem(item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 0, item)

            item = passed_signal[key]['mode']
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 1, item)

            item = passed_signal[key]['next_wp']
            item = QTableWidgetItem("Waypoint " + str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 2, item)

            item = passed_signal[key]['tof']
            item = QTableWidgetItem(str(timedelta(seconds=item)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 3, item)

            item = passed_signal[key]['altitude']
            item = QTableWidgetItem(str(item) + " m")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 4, item)

            item = passed_signal[key]['voltage']
            item = QTableWidgetItem(str(item) + " V")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 5, item)

            item = passed_signal[key]['current']
            item = QTableWidgetItem(str(item) + " A")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 6, item)

            item = passed_signal[key]['relay_sw']
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 7, item)

            item = passed_signal[key]['engine_sw']
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 8, item)

            item = passed_signal[key]['connection']
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 9, item)

            self.widget_map.add_drone(
                passed_signal[key]['name'],
                passed_signal[key]['latitude'],
                passed_signal[key]['longitude'],
                passed_signal[key]['heading'],
                passed_signal[key]['track'],
                passed_signal[key]['mode'],
                self.ctx)

        self.widget_map.update_map()
#        self.tableWidget.currentRow().connect(self.find_row)


        # # updating the lcd display
        # self.label_seluav.setText(str(self.name))
        # self.lcdNumber_altitude.display(self.altitude)
        # self.lcdNumber_vspeed.display(self.vspeed)
        # self.lcdNumber_airspeed.display(self.airspeed)
        # self.lcdNumber_gndspeed.display(self.gndspeed)
        # self.lcdNumber_voltage.display(self.voltage)
        # self.lcdNumber_current.display(self.current)


        # self.widget_hud.roll_angle = self.roll_angle
        # self.widget_hud.pitch_angle = self.pitch_angle
        # self.widget_hud.gndspeed = self.gndspeed
        # self.widget_hud.airspeed = self.airspeed
        # self.widget_hud.altitude = self.altitude
        # self.widget_hud.vspeed = self.vspeed
        # self.widget_hud.heading = self.heading
        # self.widget_hud.arm = self.arm
        # self.widget_hud.gnss_fix = self.gnss_fix
        # self.widget_hud.mode= self.mode
        # self.widget_hud.repaint()


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

    signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.rate = None
        self.timer = None
        self.vehicles_list = {}

    @pyqtSlot()
    def run(self):
        self.vehicles_list = {}

        url = "{}attitude_data".format(URL_BASE)
        attitude_data = requests.get(url).json()

        url = "{}sys_status".format(URL_BASE)
        sys_status = requests.get(url).json()

        url = "{}sys_data".format(URL_BASE)
        sys_data = requests.get(url).json()

        url = "{}sys_info".format(URL_BASE)
        sys_info = requests.get(url).json()

        url = "{}map_data".format(URL_BASE)
        map_data = requests.get(url).json()

        all_signals = [attitude_data, sys_status, sys_data, sys_info, map_data]

        for item in all_signals:
            for key, values in item.items():
                if key not in self.vehicles_list:
                    self.vehicles_list[key] = values
                self.vehicles_list[key].update(values)

        self.signal.emit(self.vehicles_list)
        self.timer.start(self.rate)

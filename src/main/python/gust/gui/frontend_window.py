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

        self._conWindow = None
        self._confirmationWindow = None
        self._sensorsWindow = None

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

        header = self.tableWidget.horizontalHeader()
        header.setMinimumSectionSize(120)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        self.once_clicked = False
        self.tableWidget.cellClicked.connect(self.item_clicked)

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

    @pyqtSlot()
    def clicked_addvehicle(self):
        if self._conWindow is None:
            self._conWindow = con_window.ConWindow(
                self.ctx)
        self._conWindow.show()

        # adding a row in the table
        rowPos = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPos)

    @pyqtSlot()
    def clicked_engineOff(self):
        if self._confirmationWindow is None:
            self._confirmationWindow = confirmation_window.ConfirmationWindow(
                self.ctx)
        self._confirmationWindow.show()

    @pyqtSlot()
    def clicked_RTL(self):
        if self._confirmationWindow is None:
            self._confirmationWindow = confirmation_window.ConfirmationWindow(
                self.ctx)
        self._confirmationWindow.show()

    @pyqtSlot()
    def clicked_disarm(self):
        if self._confirmationWindow is None:
            self._confirmationWindow = confirmation_window.ConfirmationWindow(
                self.ctx)
        self._confirmationWindow.show()

    @pyqtSlot()
    def clicked_sensors(self):
        if self._sensorsWindow is None:
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

    def update_frame(self, passed_signal):

        self.widget_map.clear_drone_list()
        self.flight_params = passed_signal

        # filling up the table
        for key in self.flight_params:
            rowPos = int(key) - 1

            item = self.flight_params[key]['name']
            item = QTableWidgetItem(item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 0, item)

            item = self.flight_params[key]['flt_mode']
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 1, item)

            item = self.flight_params[key]['next_wp']
            item = QTableWidgetItem("Waypoint " + str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 2, item)

            item = self.flight_params[key]['tof']
            item = QTableWidgetItem(str(timedelta(seconds=item)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 3, item)

            item = self.flight_params[key]['altitude']
            item = QTableWidgetItem(str(item) + " m")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 4, item)

            item = self.flight_params[key]['voltage']
            item = QTableWidgetItem(str(item) + " V")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 5, item)

            item = self.flight_params[key]['current']
            item = QTableWidgetItem(str(item) + " A")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 6, item)

            item = self.flight_params[key]['relay_sw']
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 7, item)

            item = self.flight_params[key]['engine_sw']
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 8, item)

            item = self.flight_params[key]['connection']
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 9, item)

            self.widget_map.add_drone(
                self.flight_params[key]['name'],
                self.flight_params[key]['latitude'],
                self.flight_params[key]['longitude'],
                self.flight_params[key]['heading'],
                self.flight_params[key]['track'],
                self.flight_params[key]['flt_mode'],
                self.ctx)

        self.widget_map.update_map()

        if self.once_clicked:
            self.vehicle_selected()

    def item_clicked(self, row, column):
        self.once_clicked = True
        self.row = row
        self.vehicle_selected()

    def vehicle_selected(self):
        key_val = self.row
        key_val += 1
        key_pos = str(key_val)

        # updating the lcd display
        self.label_seluav.setText(str(self.flight_params[key_pos]['name']))
        self.lcdNumber_altitude.display(self.flight_params[key_pos]['altitude'])
        self.lcdNumber_vspeed.display(self.flight_params[key_pos]['vspeed'])
        self.lcdNumber_airspeed.display(self.flight_params[key_pos]['airspeed'])
        self.lcdNumber_gndspeed.display(self.flight_params[key_pos]['gndspeed'])
        self.lcdNumber_voltage.display(self.flight_params[key_pos]['voltage'])
        self.lcdNumber_current.display(self.flight_params[key_pos]['current'])

        self.widget_hud.roll_angle = self.flight_params[key_pos]['roll_angle']
        self.widget_hud.pitch_angle = self.flight_params[key_pos]['pitch_angle']
        self.widget_hud.gndspeed = self.flight_params[key_pos]['gndspeed']
        self.widget_hud.airspeed = self.flight_params[key_pos]['airspeed']
        self.widget_hud.altitude = self.flight_params[key_pos]['altitude']
        self.widget_hud.vspeed = self.flight_params[key_pos]['vspeed']
        self.widget_hud.heading = self.flight_params[key_pos]['heading']
        self.widget_hud.arm = self.flight_params[key_pos]['arm']
        self.widget_hud.gnss_fix = self.flight_params[key_pos]['gnss_fix']
        self.widget_hud.mode = self.flight_params[key_pos]['flt_mode']
        self.widget_hud.repaint()

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

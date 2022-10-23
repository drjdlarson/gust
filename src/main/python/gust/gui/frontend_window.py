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
from PyQt5. QtWidgets import QMainWindow, QMessageBox, QHeaderView, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex, pyqtSignal, QThreadPool, QThread, QTimer
from PyQt5.QtGui import QIntValidator, QTextCursor
import requests
from gust.gui.ui.gustClient import Ui_MainWindow_main
from gust.gui import con_window, log_window, sensors_window
from gust.gui import engineoff_confirmation, disconnect_confirmation, rtl_confirmation, disarm_confirmation
from gust.gui import rc_window, servo_window
from gust.gui.ui.map_widget import MapWidget
from gust.gui.ui.attitude_ind_widget import pyG5AIWidget
from gust.gui.msg_decoder import MessageDecoder as msg_decoder
from gust.wsgi_apps.api.url_bases import BASE, DRONE


URL_BASE = "http://localhost:8000/{}/".format(BASE)
DRONE_BASE = "{}{}/".format(URL_BASE, DRONE)
FILES = ["home", "pos", "spos", "rtl_pos"]

class FrontendWindow(QMainWindow, Ui_MainWindow_main):
    """Main interface for the frontend window."""

    def __init__(self, ctx):
        super().__init__()
        self.timer = None

        self._conWindow = None
        self._sensorsWindow = None
        self._rcWindow = None
        self._servoWindow = None

        self.manager = DataManager()
        self.ctx = ctx
        self.setupUi(self)


        # Pushbuttons
        self.pushButton_addvehicle.clicked.connect(self.clicked_addvehicle)
        self.pushButton_engineOff.clicked.connect(self.clicked_engineOff)
        self.pushButton_RTL.clicked.connect(self.clicked_RTL)
        self.pushButton_disarm.clicked.connect(self.clicked_disarm)

        self.pushButton_sensors.clicked.connect(self.clicked_sensors)
        self.pushButton_rc.clicked.connect(self.clicked_rc)
        self.pushButton_servo.clicked.connect(self.clicked_servo)
        self.pushButton_tune.clicked.connect(self.clicked_tune)

        # Setting few features of the table
        header = self.tableWidget.horizontalHeader()
        header.setMinimumSectionSize(120)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        self.once_clicked = False
        self.tableWidget.cellClicked.connect(self.item_clicked)

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)
        self.widget_map.setup_qml(self.ctx)
        self.widget_hud.setup_hud_ui(self.ctx)


    @pyqtSlot()
    def clicked_addvehicle(self):

        url = "{}get_available_ports".format(DRONE_BASE)
        ports = requests.get(url).json()

        if self._conWindow is None:
            self._conWindow = con_window.ConWindow(
                self.ctx, ports['ports'])

        if self._conWindow.exec_():
            # adding a row in the table
            rowPos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPos)
            self.update_request()


    @pyqtSlot()
    def clicked_engineOff(self):
        win = engineoff_confirmation.EngineOffConfirmation(
            self.ctx)
        win.exec_()


    @pyqtSlot()
    def clicked_RTL(self):
        win = rtl_confirmation.RTLConfirmation(
            self.ctx)
        win.exec_()


    @pyqtSlot()
    def clicked_disarm(self):
        win = disarm_confirmation.DisarmConfirmation(
            self.ctx)
        win.exec_()

    @pyqtSlot()
    def clicked_rc(self):
        if self._rcWindow is None:
            self._rcWindow = rc_window.RCWindow(
                self.ctx)
        self._rcWindow.show()

    @pyqtSlot()
    def clicked_servo(self):
        if self._servoWindow is None:
            self._servoWindow = servo_window.ServoWindow(
                self.ctx)
        self._servoWindow.show()

    @pyqtSlot()
    def clicked_tune(self):
        pass

    @pyqtSlot()
    def clicked_sensors(self):
        if self._sensorsWindow is None:
            self._sensorsWindow = sensors_window.SensorsWindow(
                self.ctx, parent=self)
        self._sensorsWindow.show()


    @pyqtSlot()
    def clicked_disconnect(self):
        button = self.sender()
        if button:
            sel_row = self.tableWidget.indexAt(button.pos()).row()
            name = self.tableWidget.item(sel_row, 1).text()
            win = disconnect_confirmation.DisconnectConfirmation(
                name, self.ctx)
            res = win.exec_()
            if res:
                self.tableWidget.removeRow(sel_row)
                self.clean_hud_and_lcd()
                self.delete_map_icons(name)

    def delete_map_icons(self, name):
        for file in FILES:
            filename = name + '_' + file + '.png'
            icon_file = self.ctx.get_resource('map_widget/' + filename)
            os.remove(icon_file)

    def update_request(self):
        if self.timer is None:
            self.timer = QTimer()
            self.manager.timer = self.timer
            self.manager.rate = 750
            self.timer.timeout.connect(self.manager.run)
            self.manager.signal.connect(self.update_frame)
            self.timer.start(750)

    def update_frame(self, passed_signal):

        self.widget_map.clear_drone_list()
        self.flight_params = passed_signal

        # filling up the table
        for key in self.flight_params:
            rowPos = int(key) - 1

            item = QTableWidgetItem()
            color = self.flight_params[key]['color']
            item.setBackground(QtGui.QColor(color))
            self.tableWidget.setItem(rowPos, 0, item)


            item = self.flight_params[key]['name']
            item = QTableWidgetItem(item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 1, item)

            item = self.flight_params[key]['flight_mode']
            item = msg_decoder.findMode(int(item))
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 2, item)

            item = self.flight_params[key]['next_wp']
            item = QTableWidgetItem("Waypoint " + str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 3, item)

            item = int(self.flight_params[key]['tof'])
            item = QTableWidgetItem(str(timedelta(seconds=item)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 4, item)

            item = self.flight_params[key]['relative_alt']
            item = QTableWidgetItem(str(item) + " m")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 5, item)

            item = self.flight_params[key]['voltage']
            item = QTableWidgetItem(str(item) + " V")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 6, item)

            item = self.flight_params[key]['current']
            item = QTableWidgetItem(str(item) + " A")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 7, item)

            item = self.flight_params[key]['relay_sw']
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 8, item)

            item = self.flight_params[key]['engine_sw']
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 9, item)

            # self.con_status will be 1 or 0.
            self.con_status = self.flight_params[key]['connection']
            self.disconnect_button = QPushButton("Disconnect")
            self.disconnect_button.clicked.connect(self.clicked_disconnect)
            self.tableWidget.setCellWidget(rowPos, 10, self.disconnect_button)


            self.widget_map.add_drone(
                self.flight_params[key]['name'],
                self.flight_params[key]['home_lat'],
                self.flight_params[key]['home_lon'],
                self.flight_params[key]['latitude'],
                self.flight_params[key]['longitude'],
                self.flight_params[key]['heading'],
                self.flight_params[key]['track'],
                self.flight_params[key]['flight_mode'],
                )

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

        # Updating the lcd display
        self.label_seluav.setText(str(self.flight_params[key_pos]['name']))
        self.lcdNumber_altitude.display(self.flight_params[key_pos]['relative_alt'])
        self.lcdNumber_vspeed.display(self.flight_params[key_pos]['vspeed'])
        self.lcdNumber_airspeed.display(self.flight_params[key_pos]['airspeed'])
        self.lcdNumber_gndspeed.display(self.flight_params[key_pos]['gndspeed'])
        self.lcdNumber_voltage.display(self.flight_params[key_pos]['voltage'])
        self.lcdNumber_current.display(self.flight_params[key_pos]['current'])

        # Updating the Attitude Indicator
        self.widget_hud.roll_angle = self.flight_params[key_pos]['roll_angle']
        self.widget_hud.pitch_angle = self.flight_params[key_pos]['pitch_angle']
        self.widget_hud.gndspeed = self.flight_params[key_pos]['gndspeed']
        self.widget_hud.airspeed = self.flight_params[key_pos]['airspeed']
        self.widget_hud.altitude = self.flight_params[key_pos]['relative_alt']
        self.widget_hud.vspeed = self.flight_params[key_pos]['vspeed']
        self.widget_hud.heading = self.flight_params[key_pos]['heading']
        self.widget_hud.arm = self.flight_params[key_pos]['armed']
        self.widget_hud.gnss_fix = self.flight_params[key_pos]['gnss_fix']
        self.widget_hud.mode = self.flight_params[key_pos]['flight_mode']
        self.widget_hud.alpha = self.flight_params[key_pos]['alpha']
        self.widget_hud.beta = self.flight_params[key_pos]['beta']
        self.widget_hud.sat_count = self.flight_params[key_pos]['satellites_visible']
        self.widget_hud.repaint()

    def clean_hud_and_lcd(self):

        # Cleaning the LCD display
        self.label_seluav.setText("Current Vehicle Name")
        self.lcdNumber_altitude.display(0)
        self.lcdNumber_vspeed.display(0)
        self.lcdNumber_airspeed.display(0)
        self.lcdNumber_gndspeed.display(0)
        self.lcdNumber_voltage.display(0)
        self.lcdNumber_current.display(0)

        self.widget_hud.clean_hud()
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

        url = "{}sys_data".format(DRONE_BASE)
        sys_data = requests.get(url).json()

        url = "{}attitude_data".format(DRONE_BASE)
        attitude_data = requests.get(url).json()

        url = "{}pos_data".format(DRONE_BASE)
        pos_data = requests.get(url).json()

        url = "{}sys_info".format(DRONE_BASE)
        sys_info = requests.get(url).json()

        all_signals = [sys_data, attitude_data, pos_data, sys_info]

        for item in all_signals:
            for key, values in item.items():
                if key not in self.vehicles_list:
                    self.vehicles_list[key] = values
                self.vehicles_list[key].update(values)

        self.signal.emit(self.vehicles_list)
        self.timer.start(self.rate)

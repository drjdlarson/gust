# !/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:02:36 2022

@author: lagerprocessor
"""

import sys
import os
import time
import pathlib
from datetime import timedelta
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QHeaderView,
    QTableWidgetItem,
    QPushButton,
)
from PyQt5.QtCore import (
    Qt,
    pyqtSlot,
    QModelIndex,
    pyqtSignal,
    QThreadPool,
    QThread,
    QTimer,
)
from PyQt5.QtGui import QIntValidator, QTextCursor
import requests
from gust.gui.ui.gustClient import Ui_MainWindow_main
from gust.gui import (
    con_window,
    log_window,
    sensors_window,
    planning_selection_window,
    commands_window,
    start_sil_window,
)
from gust.gui import (
    engineoff_confirmation,
    disconnect_confirmation,
    rtl_confirmation,
    disarm_confirmation,
)
from utilities import ConnSettings as conn_settings
from gust.gui.ui.map_widget import MapWidget
from gust.gui.ui.attitude_ind_widget import pyG5AIWidget
from gust.gui.msg_decoder import MessageDecoder as msg_decoder
from wsgi_apps.api.url_bases import BASE, DRONE


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
        self._cmdWindow = None
        self._servoWindow = None
        self._planningWindow = None
        self._sil_window = None

        self.sil_vehicles = []
        self._continue_updating_data = False
        self.flight_params = None

        self.manager = DataManager()
        self.ctx = ctx
        self.setupUi(self)

        # Pushbuttons
        self.pushButton_addvehicle.clicked.connect(self.clicked_addvehicle)
        self.pushButton_sil.clicked.connect(self.clicked_sil)

        self.pushButton_engineOff.clicked.connect(self.clicked_engineOff)
        self.pushButton_RTL.clicked.connect(self.clicked_RTL)
        self.pushButton_disarm.clicked.connect(self.clicked_disarm)

        self.pushButton_refresh_map.clicked.connect(self.clicked_refresh_map)
        self.pushButton_sensors.clicked.connect(self.clicked_sensors)
        self.pushButton_commands.clicked.connect(self.clicked_commands)
        self.pushButton_tune.clicked.connect(self.clicked_tune)
        self.pushButton_sensors.clicked.connect(self.clicked_sil)
        self.pushButton_planning.clicked.connect(self.clicked_planning)

        self.comboBox_saved_locations.currentTextChanged.connect(self.recenter_map)

        self.once_clicked = False
        self.tableWidget.cellClicked.connect(self.item_clicked)

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)
        self.widget_map.setup_qml(self.ctx)
        self.widget_hud.setup_hud_ui(self.ctx)

        url = "{}get_saved_locations".format(DRONE_BASE)
        self.saved_locations = requests.get(url).json()
        self.comboBox_saved_locations.addItems(self.saved_locations.keys())

    def recenter_map(self):
        center_location = self.comboBox_saved_locations.currentText()
        center_coords = self.saved_locations[center_location]
        self.widget_map.recenter_map(center_coords)

    @pyqtSlot()
    def clicked_addvehicle(self):

        url = "{}get_available_ports".format(DRONE_BASE)
        ports = requests.get(url).json()

        url = "{}get_used_colors".format(DRONE_BASE)
        used_colors = requests.get(url).json()

        if self._conWindow is None:
            self._conWindow = con_window.ConWindow(
                self.ctx, ports["ports"], used_colors["used_colors"], self.sil_vehicles
            )

        if self._conWindow.exec_():
            time.sleep(2.0)
            self._continue_updating_data = True

            # adding a row in the table
            rowPos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPos)
            self.update_request()
        self._conWindow = None

    @pyqtSlot()
    def clicked_engineOff(self):
        win = engineoff_confirmation.EngineOffConfirmation(self.ctx)
        win.exec_()

    @pyqtSlot()
    def clicked_RTL(self):
        win = rtl_confirmation.RTLConfirmation(self.ctx)
        win.exec_()

    @pyqtSlot()
    def clicked_disarm(self):
        win = disarm_confirmation.DisarmConfirmation(self.ctx)
        win.exec_()

    @pyqtSlot()
    def clicked_tune(self):
        pass

    @pyqtSlot()
    def clicked_sensors(self):
        if self._sensorsWindow is None:
            self._sensorsWindow = sensors_window.SensorsWindow(self.ctx, parent=self)
        self._sensorsWindow.show()

    def clicked_sil(self):
        if self._sil_window is None:
            self._sil_window = start_sil_window.StartSILWindow(
                self.ctx, self.saved_locations
            )
            self._sil_window.signal.connect(self.add_sil_vehicle)

        self._sil_window.exec_()
        self._sil_window = None

    @pyqtSlot()
    def clicked_planning(self):
        if self._planningWindow is None:
            self._planningWindow = planning_selection_window.PlanningSelectionWindow(
                self.ctx, parent=self
            )
        self._planningWindow.show()
        self._planningWindow = None

    @pyqtSlot()
    def clicked_commands(self):
        if self._cmdWindow is None:
            self._cmdWindow = commands_window.CommandsManager(self.ctx, parent=self)
        self._cmdWindow.show()

    @pyqtSlot()
    def clicked_disconnect(self):
        button = self.sender()
        if button:
            sel_row = self.tableWidget.indexAt(button.pos()).row()
            name = self.tableWidget.item(sel_row, 1).text()
            win = disconnect_confirmation.DisconnectConfirmation(name, self.ctx)
            res = win.exec_()
            if res:
                self.tableWidget.removeRow(sel_row)
                self._continue_updating_data = self.tableWidget.rowCount() > 0
                self.clean_hud_and_lcd()
                print("vehicle disconnecting is {}".format(name))
                self.widget_map.remove_vehicle_from_map(name)

    def add_sil_vehicle(self, sil_name):
        self.sil_vehicles.append(sil_name)

    def update_request(self):
        if self.timer is None:
            self.timer = QTimer()
            self.manager.timer = self.timer
            self.manager.rate = 100
            self.timer.timeout.connect(self.manager.run)
            self.manager.signal.connect(self.update_frame)
            if self._continue_updating_data:
                self.timer.start(100)

    def update_frame(self, passed_signal):

        self.flight_params = passed_signal

        # filling up the table
        for key in self.flight_params:
            rowPos = int(key) - 1
            # rowPos = int(key)

            item = QTableWidgetItem()
            color = self.flight_params[key]["color"]
            item.setBackground(QtGui.QColor(color))
            self.tableWidget.setItem(rowPos, 0, item)

            item = self.flight_params[key]["name"]
            item = QTableWidgetItem(item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 1, item)

            item = self.flight_params[key]["flight_mode"]
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 2, item)

            item = self.flight_params[key]["next_wp"]
            item = QTableWidgetItem("Waypoint " + str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 3, item)

            item = int(self.flight_params[key]["tof"])
            item = QTableWidgetItem(str(timedelta(seconds=item)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 4, item)

            item = self.flight_params[key]["relative_alt"]
            item = QTableWidgetItem(str(item) + " m")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 5, item)

            item = self.flight_params[key]["voltage"]
            item = QTableWidgetItem(str(item) + " V")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 6, item)

            item = self.flight_params[key]["current"]
            item = QTableWidgetItem(str(item) + " A")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 7, item)

            item = self.flight_params[key]["relay_sw"]
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 8, item)

            item = self.flight_params[key]["engine_sw"]
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 9, item)

            # self.con_status will be 1 or 0.
            self.disconnect_button = QPushButton("Disconnect")
            self.disconnect_button.clicked.connect(self.clicked_disconnect)
            self.tableWidget.setCellWidget(rowPos, 10, self.disconnect_button)

            self.widget_map.add_drone(
                self.flight_params[key]["name"],
                self.flight_params[key]["color"],
                self.flight_params[key]["home_lat"],
                self.flight_params[key]["home_lon"],
                self.flight_params[key]["latitude"],
                self.flight_params[key]["longitude"],
                self.flight_params[key]["yaw"],
                self.flight_params[key]["heading"],
                self.flight_params[key]["flight_mode"],
            )

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
        self.label_seluav.setText(str(self.flight_params[key_pos]["name"]))
        self.lcdNumber_altitude.display(self.flight_params[key_pos]["relative_alt"])
        self.lcdNumber_vspeed.display(self.flight_params[key_pos]["vspeed"])
        self.lcdNumber_airspeed.display(self.flight_params[key_pos]["airspeed"])
        self.lcdNumber_heading.display(self.flight_params[key_pos]["yaw"])
        self.lcdNumber_voltage.display(self.flight_params[key_pos]["voltage"])
        self.lcdNumber_current.display(self.flight_params[key_pos]["current"])

        # Updating the Attitude Indicator
        self.widget_hud.roll_angle = self.flight_params[key_pos]["roll_angle"]
        self.widget_hud.pitch_angle = self.flight_params[key_pos]["pitch_angle"]
        self.widget_hud.gndspeed = self.flight_params[key_pos]["gndspeed"]
        self.widget_hud.airspeed = self.flight_params[key_pos]["airspeed"]
        self.widget_hud.altitude = self.flight_params[key_pos]["relative_alt"]
        self.widget_hud.vspeed = self.flight_params[key_pos]["vspeed"]
        self.widget_hud.yaw = self.flight_params[key_pos]["yaw"]
        self.widget_hud.arm = self.flight_params[key_pos]["armed"]
        self.widget_hud.gnss_fix = self.flight_params[key_pos]["gnss_fix"]
        self.widget_hud.mode = self.flight_params[key_pos]["flight_mode"]
        self.widget_hud.alpha = self.flight_params[key_pos]["alpha"]
        self.widget_hud.beta = self.flight_params[key_pos]["beta"]
        self.widget_hud.sat_count = self.flight_params[key_pos]["satellites_visible"]
        self.widget_hud.repaint()

    def clicked_refresh_map(self):
        # self.recenter_map()
        if self.flight_params is not None:
            if len(self.flight_params) != 0:
                url = "{}download_wp".format(DRONE_BASE)
                all_waypoints = requests.get(url).json()

                self.widget_map.display_missions(all_waypoints)

    def clean_hud_and_lcd(self):
        # Cleaning the LCD display
        self.label_seluav.setText("Current Vehicle Name")
        self.lcdNumber_altitude.display(0)
        self.lcdNumber_vspeed.display(0)
        self.lcdNumber_airspeed.display(0)
        self.lcdNumber_heading.display(0)
        self.lcdNumber_voltage.display(0)
        self.lcdNumber_current.display(0)

        self.widget_hud.clean_hud()
        self.tableWidget.clearContents()


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

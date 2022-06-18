#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:02:36 2022

@author: lagerprocessor
"""

import sys
import os
from datetime import timedelta
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5. QtWidgets import QMainWindow, QMessageBox, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, QModelIndex, pyqtSignal, QThreadPool
from PyQt5.QtGui import QIntValidator, QTextCursor
import requests
from gust.gui.ui.gustClient import Ui_MainWindow_main
from gust.gui import con_window, confirmation_window, log_window, sensors_window
from gust.gui.ui.map_widget import MapWidget
from gust.gui.ui.attitude_ind_widget import pyG5Widget

URL_BASE="http://localhost:8000/api/"

class FrontendWindow(QMainWindow, Ui_MainWindow_main):
    """Main interface for the frontend window."""

    def __init__(self, ctx):
        super().__init__()
        self.ctx=ctx
        self.setupUi(self)

        self.map_widget=MapWidget()
        self.att_ind_widget=pyG5Widget()

        #Pushbuttons
        self.pushButton_addvehicle.clicked.connect(self.clicked_addvehicle)
        self.pushButton_engineOff.clicked.connect(self.clicked_engineOff)
        self.pushButton_RTL.clicked.connect(self.clicked_RTL)
        self.pushButton_disarm.clicked.connect(self.clicked_disarm)
        self.pushButton_sensors.clicked.connect(self.clicked_sensors)

        self.pushButton_update.clicked.connect(self.clicked_update)
        self.pushButton_default.clicked.connect(self.clicked_default)

        self._conWindow=None
        self._confirmationWindow=None
        self._sensorsWindow=None

        header=self.tableWidget.horizontalHeader()
        header.setMinimumSectionSize(120)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)



    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

    @pyqtSlot()
    def clicked_addvehicle(self):
        self._conWindow=con_window.ConWindow(
            self.ctx)
        self._conWindow.show()

        #adding a row in the table
        rowPos=self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPos)

    @pyqtSlot()
    def clicked_engineOff(self):
        self._confirmationWindow=confirmation_window.ConfirmationWindow(
            self.ctx)
        self._confirmationWindow.show()

    @pyqtSlot()
    def clicked_RTL(self):
        self._confirmationWindow=confirmation_window.ConfirmationWindow(
            self.ctx)
        self._confirmationWindow.show()

    @pyqtSlot()
    def clicked_disarm(self):
        self._confirmationWindow=confirmation_window.ConfirmationWindow(
            self.ctx)
        self._confirmationWindow.show()

    @pyqtSlot()
    def clicked_sensors(self):
        self._sensorsWindow=sensors_window.SensorsWindow(
            self.ctx)
        self._sensorsWindow.show()

    def clicked_update(self):

        #selected drone name
        url="{}seluav".format(URL_BASE)
        r=requests.get(url).json()
        name=r['VehicleName']

        #altitude
        url="{}altitude".format(URL_BASE)
        r=requests.get(url).json()
        altitude=r['Altitude']

        #vspeed
        url="{}vspeed".format(URL_BASE)
        r=requests.get(url).json()
        vspeed=r['Vspeed']

        #airspeed
        url="{}airspeed".format(URL_BASE)
        r=requests.get(url).json()
        airspeed=r['Airspeed']

        #Ground Speed
        url="{}gndspeed".format(URL_BASE)
        r=requests.get(url).json()
        gndspeed=r['Gndspeed']

        #Voltage
        url="{}voltage".format(URL_BASE)
        r=requests.get(url).json()
        voltage=r['Voltage']

        #current
        url="{}current".format(URL_BASE)
        r=requests.get(url).json()
        current=r['Current']

        #engine switch
        url="{}engine_sw".format(URL_BASE)
        r=requests.get(url).json()
        engine_sw=r['Engine Status']

        #relay switch
        url="{}relay_sw".format(URL_BASE)
        r=requests.get(url).json()
        relay_sw=r['Relay Status']

        #mode state
        url="{}mode".format(URL_BASE)
        r=requests.get(url).json()
        mode=r['Mode']

        #arm state
        url="{}arm".format(URL_BASE)
        r=requests.get(url).json()
        arm=r['Arm']

        #gnss fix
        url="{}gnss_fix".format(URL_BASE)
        r=requests.get(url).json()
        gnss_fix=r['Gnss_fix']

        #roll angle
        url="{}roll_angle".format(URL_BASE)
        r=requests.get(url).json()
        roll_angle=r['Roll_angle']

        #pitch angle
        url="{}pitch_angle".format(URL_BASE)
        r=requests.get(url).json()
        pitch_angle=r['Pitch_angle']

        #heading
        url="{}heading".format(URL_BASE)
        r=requests.get(url).json()
        heading=r['Heading']

        #next waypoint
        url="{}next_wp".format(URL_BASE)
        r=requests.get(url).json()
        next_wp=r['Next_wp']

        #time of flight
        url="{}tof".format(URL_BASE)
        r=requests.get(url).json()
        tof=r['Tof']
        tof_hms=timedelta(seconds=tof)

        #connection
        url="{}connection".format(URL_BASE)
        r=requests.get(url).json()
        connection=r['Connection']

        #track
        url="{}track".format(URL_BASE)
        r=requests.get(url).json()
        track=r['Track']

        #latitude
        url="{}latitude".format(URL_BASE)
        r=requests.get(url).json()
        latitude=r['Latitude']

        #Longitude
        url="{}longitude".format(URL_BASE)
        r=requests.get(url).json()
        longitude=r['Longitude']




        #updating the lcd display
        self.label_seluav.setText(str(name))
        self.lcdNumber_altitude.display(altitude)
        self.lcdNumber_vspeed.display(vspeed)
        self.lcdNumber_airspeed.display(airspeed)
        self.lcdNumber_gndspeed.display(gndspeed)
        self.lcdNumber_voltage.display(voltage)
        self.lcdNumber_current.display(current)


        #self.update_table(self)
        rowPos=self.tableWidget.rowCount()
        rowPos-=1
        item=QTableWidgetItem(name)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 0, item)
        item=QTableWidgetItem(str(mode))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 1, item)
        item=QTableWidgetItem("Waypoint "+str(next_wp))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 2, item)
        item=QTableWidgetItem(str(tof_hms))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 3, item)
        item=QTableWidgetItem(str(altitude)+ " m")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 4, item)
        item=QTableWidgetItem(str(voltage)+ " V")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 5, item)
        item=QTableWidgetItem(str(current)+ " A")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 6, item)
        item=QTableWidgetItem(str(relay_sw))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 7, item)
        item=QTableWidgetItem(str(engine_sw))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 8, item)
        item=QTableWidgetItem(str(connection))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(rowPos, 9, item)


    def clicked_default(self):
        self.label_seluav.setText("Current Vehicle Name")
        self.lcdNumber_altitude.display(100)
        self.lcdNumber_vspeed.display(100)
        self.lcdNumber_airspeed.display(100)
        self.lcdNumber_gndspeed.display(100)
        self.lcdNumber_voltage.display(100)
        self.lcdNumber_current.display(100)

        self.tableWidget.clearContents()

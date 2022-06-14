#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:02:36 2022

@author: lagerprocessor
"""

import sys
import os
from functools import partial
from PyQt5. QtWidgets import QMainWindow, QMessageBox, QHeaderView
from PyQt5.QtCore import pyqtSlot, QModelIndex, pyqtSignal, QThreadPool
from PyQt5.QtGui import QIntValidator, QTextCursor
import requests
from gust.gui.ui.gustClient import Ui_MainWindow_main
from gust.gui import con_window, confirmation_window, log_window, sensors_window

URL_BASE="http://localhost:8000/api/"

class FrontendWindow(QMainWindow, Ui_MainWindow_main):
    """Main interface for the frontend window."""

    def __init__(self, ctx):
        super().__init__()
        self.ctx=ctx
        self.setupUi(self)

        #Pushbuttons
        self.pushButton_addvehicle.clicked.connect(self.clicked_addvehicle)
        self.pushButton_engineOff.clicked.connect(self.clicked_engineOff)
        self.pushButton_RTL.clicked.connect(self.clicked_RTL)
        self.pushButton_disarm.clicked.connect(self.clicked_disarm)
        self.pushButton_sensors.clicked.connect(self.clicked_sensors)

        self._conWindow=None
        self._confirmationWindow=None
        self._sensorsWindow=None

        # header=self.tableWidget.horizontalHeader()
        # header.setMinimumSectionSize(120)
        # header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # header.setStretchLastSection(True)



    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

    @pyqtSlot()
    def clicked_addvehicle(self):
        self._conWindow=con_window.ConWindow(
            self.ctx)

        self._conWindow.show()


        # #print('clicked client')
        # url = "{}addvehicle".format(URL_BASE)
        # print(url)
        # r = requests.get(url).json()
        # answer = r['Newvehicle']
        # QMessageBox.question(self, "Message", "Answer: {}".format(str(answer)),
        #                       QMessageBox.Ok, QMessageBox.Ok)

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

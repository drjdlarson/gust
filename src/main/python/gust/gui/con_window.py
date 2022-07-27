#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 12:36:33 2022

@author: lagerprocessor
"""

import sys
import os
from functools import partial
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot, QModelIndex, pyqtSignal, QThreadPool
from PyQt5.QtGui import QIntValidator, QTextCursor
import requests
from gust.gui.ui.conn import Ui_MainWindow


URL_BASE = "http://localhost:8000/api/"


class ConWindow(QMainWindow, Ui_MainWindow):
    """Main interface for the connection window"""

    def __init__(self, ctx, ports):
        super().__init__()
        self.ctx = ctx
        self.setupUi(self)

        self.comboBox_port.addItems(ports)

        self.pushButton_connect.clicked.connect(self.clicked_connect)
        self.pushButton_cancel.clicked.connect(self.clicked_cancel)

    def clicked_cancel(self):
        self.close()

    def clicked_connect(self):

        port_name = self.comboBox_port.currentText()
        name = self.lineEdit_nameinput.text()
        url = "{}connect_drone".format(URL_BASE)

        if len(port_name) > 0 or len(name) > 0:
            url += '?'
            added_data = False
            if len(port_name) > 0:
                url += "port=" + port_name.replace('/', '%2F')
                added_data = True
            if len(name) > 0:
                if added_data:
                    url += "&"
                url += "name=" + name.replace(' ', '_')
                added_data = True
        conn = requests.get(url).json()

        if conn['success']:
            self.close()

        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Warning")
            msgBox.setText("Unable to connect: <<{:s}>>".format(conn['msg']))
            msgBox.exec()

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

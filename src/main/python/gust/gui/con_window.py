#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 12:36:33 2022

@author: lagerprocessor
"""

import sys
import os
import pathlib
from functools import partial
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog
from PyQt5.QtCore import pyqtSlot, QModelIndex, pyqtSignal, QThreadPool
from PyQt5.QtGui import QIntValidator, QTextCursor
import requests
from gust.gui.ui.conn import Ui_MainWindow
import gust.icon_generator as icon_generator
from gust.wsgi_apps.api.url_bases import BASE, DRONE


URL_BASE = "http://localhost:8000/{}/".format(BASE)
DRONE_BASE = "{}{}/".format(URL_BASE, DRONE)
COLORS = ["red", "blue", "green", "yellow", "orange", "gray", "brown"]
RGB = [
       (255, 0, 0),
       (0, 0, 255),
       (0, 255, 0),
       (255, 255, 0),
       (255, 150, 50),
       (130, 130, 130),
       (100, 50, 0),
       ]
FILES = ["home", "pos", "spos", "rtl_pos"]
BAUD = ["9600", "38400", "56700", "115200"]

class ConWindow(QDialog, Ui_MainWindow):
    """Main interface for the connection window"""

    def __init__(self, ctx, ports):
        super().__init__()
        self.ctx = ctx
        self.setupUi(self)

        self.comboBox_port.addItems(ports)
        self.comboBox_baud.addItems(BAUD)
        self.comboBox_color.addItems(COLORS)

        self.pushButton_connect.clicked.connect(self.clicked_connect)
        self.pushButton_cancel.clicked.connect(self.clicked_cancel)

    def clicked_cancel(self):
        self.reject()

    def clicked_connect(self):

        port_name = self.comboBox_port.currentText()
        self.color_id = self.comboBox_color.currentText()
        self.baud = int(self.comboBox_baud.currentText())
        self.name = self.lineEdit_nameinput.text()
        url = "{}connect".format(DRONE_BASE)

        if len(port_name) > 0 or len(self.name) > 0:
            url += '?'
            added_data = False

            if len(port_name) > 0:
                url += "port=" + port_name.replace('/', '%2F')
                added_data = True

            if len(self.name) > 0:
                if added_data:
                    url += "&"
                url += "name=" + self.name.replace(' ', '_')
                added_data = True

            if len(self.color_id) > 0:
                if added_data:
                    url += "&"
                url += "color=" + self.color_id.replace(' ', '_')
                added_data = True

            if added_data:
                url += "&"
            url += "baud={:d}".format(self.baud)
            added_data = True

        conn = requests.get(url).json()

        msgBox = QMessageBox()

        if conn['success']:
            self.generate_icons()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Information")
            msgBox.setText("Connected to vehicle: {}".format(self.name))
            msgBox.exec()
            self.accept()

        else:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Warning")
            msgBox.setText("Failed connection: <<{:s}>>".format(conn['msg']))
            msgBox.exec()

    def generate_icons(self):

        for file in FILES:
            filename = self.ctx.get_resource('map_widget/' + file + '.png')
            for (color, rgb) in zip(COLORS, RGB):
                if self.color_id == color:
                    savename = self.name + '_' + file + '.png'
                    savepath = str(pathlib.Path(filename).parent.resolve())
                    icon_generator.prepare_icon(filename, rgb, os.path.join(savepath, savename))


    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

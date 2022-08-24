#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 12:42:21 2022

@author: lagerprocessor
"""

import sys
import os
from functools import partial
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot, QModelIndex, pyqtSignal, QThreadPool
from PyQt5.QtGui import QIntValidator, QTextCursor
import requests
from gust.gui.ui.sensors import Ui_MainWindow

URL_BASE="http://localhost:8000/api/"

class SensorsWindow(QMainWindow,Ui_MainWindow):
    """Main interface for the sensors selection window"""

    def __init__(self,ctx):
        super().__init__()
        self.setupUi(self)

        # self.pushButton_connect.clicked.connect(self.clicked_connect)


    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

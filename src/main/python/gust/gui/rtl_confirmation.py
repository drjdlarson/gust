#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 15:00:26 2022

@author: lagerprocessor
"""

import sys
import os
from functools import partial
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog
from PyQt5.QtCore import pyqtSlot, QModelIndex, pyqtSignal, QThreadPool
from PyQt5.QtGui import QIntValidator, QTextCursor
import requests
from gust.gui.ui.confirmation import Ui_MainWindow

URL_BASE = "http://localhost:8000/api/"


class RTLConfirmation(QDialog, Ui_MainWindow):
    """Main interface for the confirmation window before disconnecting"""

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setupUi(self)


        self.pushButton_cancel.clicked.connect(self.clicked_cancel)
        self.pushButton_ok.clicked.connect(self.clicked_ok)
        self.label_custom.setText("Activate RTL?")

    def clicked_ok(self):
        self.reject()

    def clicked_cancel(self):
        self.reject()

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

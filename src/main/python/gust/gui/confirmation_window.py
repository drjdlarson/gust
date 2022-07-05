#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:36:32 2022

@author: lagerprocessor
"""

import sys
import os
from functools import partial
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot, QModelIndex, pyqtSignal, QThreadPool
from PyQt5.QtGui import QIntValidator, QTextCursor
import requests
from gust.gui.ui.confirmation import Ui_MainWindow

URL_BASE = "http://localhost:8000/api/"


class ConfirmationWindow(QMainWindow, Ui_MainWindow):
    """Main interface for the confirmation window"""

    def __init__(self, ctx):
        super().__init__()
        self.setupUi(self)

        self.pushButton_cancel.clicked.connect(self.clicked_cancel)
        self.pushButton_ok.clicked.connect(self.clicked_ok)

    def clicked_ok(self):
        self.close()

    def clicked_cancel(self):
        self.close()

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

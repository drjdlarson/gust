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


URL_BASE="http://localhost:8000/api/"

class ConWindow(QMainWindow,Ui_MainWindow):
    """Main interface for the connection window"""

    def __init__(self,ctx):
        super().__init__()
        self.ctx=ctx
        self.setupUi(self)

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

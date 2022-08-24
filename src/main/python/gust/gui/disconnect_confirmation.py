#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 14:39:39 2022

@author: lagerprocessor
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:36:32 2022

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


class DisconnectConfirmation(QDialog, Ui_MainWindow):
    """Main interface for the confirmation window before disconnecting"""

    def __init__(self, name, ctx):
        super().__init__()
        self.name = name
        self.ctx = ctx
        self.setupUi(self)


        self.pushButton_cancel.clicked.connect(self.clicked_cancel)
        self.pushButton_ok.clicked.connect(self.clicked_ok)
        self.label_custom.setText("Disconnect {}?".format(name))

    def clicked_ok(self):
        url = "{}disconnect_drone".format(URL_BASE)
        url += '?' + "name=" + self.name.replace(' ', '_')
        disconn = requests.get(url).json()

        msgBox = QMessageBox()

        if disconn['success']:
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Information")
            msgBox.setText("Disconnected from vehicle: {}".format(self.name))
            msgBox.exec()
            self.accept()

        else:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Warning")
            msgBox.setText("Unable to disconnect: <<{:s}>>".format(disconn['msg']))
            msgBox.exec()



    def clicked_cancel(self):
        self.reject()

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

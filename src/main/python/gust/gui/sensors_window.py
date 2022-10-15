"""Logic for sensor selection window."""
import sys
import os
import requests
from functools import partial
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot, QModelIndex, pyqtSignal, QThreadPool
from PyQt5.QtGui import QIntValidator, QTextCursor

from gust.gui.ui.sensors import Ui_SensorsWindow
from gust.gui.zed_window import ZedWindow


class SensorsWindow(QMainWindow, Ui_SensorsWindow):
    """Main interface for the sensors selection window"""

    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.ctx = ctx
        self._zed_window = None

        self.pushButton_zed.clicked.connect(self.zed_clicked)
        # self.pushButton_connect.clicked.connect(self.clicked_connect)

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)
        self.setPalette(self.parentWidget().palette())

    def zed_clicked(self):
        self._zed_window = ZedWindow(self.ctx, parent=self.parent())

        self._zed_window.show()

        self.close()

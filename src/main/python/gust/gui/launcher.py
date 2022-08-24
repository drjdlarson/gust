import sys
import logging
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot
import requests
from time import sleep

from gust.gui.ui.launcher import Ui_Launcher
from gust.gui import backend_window
from gust.gui import frontend_window
from gust.gui import log_window
import gust.server


class Launcher(QMainWindow, Ui_Launcher):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setupUi(self)

        # connect buttons
        self.pushButton_client.clicked.connect(self.clicked_client)
        self.pushButton_server.clicked.connect(self.clicked_server)
        self.pushButton_log.clicked.connect(self.clicked_log)

        self._backendWindow = None
        self._frontendWindow= None
        self._logWindow=None

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)

    @pyqtSlot()
    def clicked_client(self):
        # print('clicked client')
        # url = "http://localhost:8000/adder/{}/{}".format(40, 2)
        # r = requests.get(url)
        # json = r.json()
        # answer = json['calc']
        # QMessageBox.question(self, "Message", "Answer: {}".format(str(answer)),
        #                      QMessageBox.Ok, QMessageBox.Ok)

        self._frontendWindow=frontend_window.FrontendWindow(
            self.ctx)

        self._frontendWindow.show()
        self.close()

    @pyqtSlot()
    def clicked_server(self):
        self._backendWindow = backend_window.BackendWindow(self.ctx)
        # fix logger so it only outputs to the new output console in the backend
        # fmt = logging.getLogger().handlers[0].formatter
        fmt = logging.Formatter('%(name)s %(levelname)s %(asctime)s - %(message)s')
        logging.getLogger().handlers = []
        hndl = logging.StreamHandler(stream=self._backendWindow)
        hndl.setFormatter(fmt)
        logging.getLogger().addHandler(hndl)

        self._backendWindow.setup()
        self._backendWindow.show()

        self.close()

    @pyqtSlot()
    def clicked_log(self):
        self._logWindow=log_window.LogWindow(
            self.ctx)
        self._logWindow.show()

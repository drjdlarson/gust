import sys
import logging
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot
import requests
from time import sleep

from gust.gui.ui.launcher import Ui_Launcher
from gust.gui import server_window
import gust.server


class Launcher(QMainWindow, Ui_Launcher):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setupUi(self)

        # connect buttons
        self.pushButton_client.clicked.connect(self.clicked_client)
        self.pushButton_server.clicked.connect(self.clicked_server)

        self._serverWindow = None

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)

    @pyqtSlot()
    def clicked_client(self):
        print('clicked client')
        url = "http://localhost:8000/adder/{}/{}".format(40, 2)
        r = requests.get(url)
        json = r.json()
        answer = json['calc']
        QMessageBox.question(self, "Message", "Answer: {}".format(str(answer)),
                             QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot()
    def clicked_server(self):
        self._serverWindow = server_window.ServerWindow(self.ctx)

        # fix logger so it only outputs to the new output console in the backend
        # fmt = logging.getLogger().handlers[0].formatter
        fmt = logging.Formatter('%(name)s %(levelname)s %(asctime)s - %(message)s')
        logging.getLogger().handlers = []
        hndl = logging.StreamHandler(stream=self._serverWindow)
        hndl.setFormatter(fmt)
        logging.getLogger().addHandler(hndl)

        self._serverWindow.setup()
        self._serverWindow.show()


        self.close()

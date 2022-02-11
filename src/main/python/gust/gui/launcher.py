import sys
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot
import requests
from time import sleep

from gust.gui.ui.launcher import Ui_Launcher
import gust.server


class Launcher(QMainWindow, Ui_Launcher):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # connect buttons
        self.pushButton_client.clicked.connect(self.clicked_client)
        self.pushButton_server.clicked.connect(self.clicked_server)

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
        print('clicked server')
        gust.server.start_server()

    def closeEvent(self, event):
        # nicely close all
        if gust.server.SERVER_PROC is not None:
            gust.server.SERVER_PROC.terminate()

        sys.stdout.flush()
        sys.stderr.flush()
        sleep(0.25)
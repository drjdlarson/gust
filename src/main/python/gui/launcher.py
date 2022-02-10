from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot
import requests

from .ui.launcher import Ui_Launcher


class Launcher(QMainWindow, Ui_Launcher):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # connect buttons
        self.pushButton_client.clicked.connect(self.client_clicked)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)

    @pyqtSlot()
    def client_clicked(self):
        print('clicked client')
        url = "http://localhost:8000/adder/{}/{}".format(40, 2)
        r = requests.get(url)
        json = r.json()
        answer = json['calc']
        QMessageBox.question( self, "Message", "Answer: {}".format(str(answer)),
                             QMessageBox.Ok, QMessageBox.Ok)

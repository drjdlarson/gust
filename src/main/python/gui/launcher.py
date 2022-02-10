from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot

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

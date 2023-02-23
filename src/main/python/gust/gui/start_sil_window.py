import requests

from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtWidgets import QMainWindow
from wsgi_apps.api.url_bases import BASE, DRONE
from gust.gui.ui.start_sil import Ui_Dialog

URL_BASE = "http://localhost:8000/{}/".format(BASE)
DRONE_BASE = "{}{}/".format(URL_BASE, DRONE)


class StartSILWindow(QDialog, Ui_Dialog):
    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)

        self.ctx = ctx
        self.setupUi(self)
        self.pushButton_start.clicked.connect(self.clicked_start)
        self.pushButton_cancel.clicked.connect(self.clicked_cancel)

    def clicked_start(self):
        # vehicle_type = self.comboBox_type.currentText()
        # home_lat = 33.2151315
        # home_lon = -87.161241651

        url = "{}start_sil".format(DRONE_BASE)
        start_sil = requests.get(url).json()

        msgBox = QMessageBox()

        if start_sil["success"]:
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Information")
            msgBox.setText("Started SIL")
            msgBox.exec()
            self.accept()

        else:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Warning")
            msgBox.setText("Failed starting SIL: <<{:s}>>".format(start_sil["msg"]))
            msgBox.exec()

    def clicked_cancel(self):
        pass

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)

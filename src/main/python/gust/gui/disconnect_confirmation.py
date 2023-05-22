"""Logic for vehicle disconnection confirmation window."""
from PyQt5.QtWidgets import QMessageBox, QDialog
import requests
from gust.gui.ui.confirmation import Ui_MainWindow
from wsgi_apps.api.url_bases import BASE, DRONE


URL_BASE = "http://localhost:8000/{}/".format(BASE)
DRONE_BASE = "{}{}/".format(URL_BASE, DRONE)


class DisconnectConfirmation(QDialog, Ui_MainWindow):
    """Main interface for the confirmation window before disconnecting."""

    def __init__(self, name, ctx):
        super().__init__()
        self.name = name
        self.ctx = ctx
        self.setupUi(self)

        # event connections
        self.pushButton_cancel.clicked.connect(self.clicked_cancel)
        self.pushButton_ok.clicked.connect(self.clicked_ok)
        self.label_custom.setText("Disconnect {}?".format(name))

    def clicked_ok(self):
        """Send the disconnect request for the vehicle"""
        url = "{}disconnect".format(DRONE_BASE)
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
        """Closes the disconnect confirmation window"""
        self.reject()

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

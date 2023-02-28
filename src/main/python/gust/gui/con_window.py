from PyQt5.QtWidgets import QMessageBox, QDialog
import requests
from gust.gui.ui.conn import Ui_MainWindow
from wsgi_apps.api.url_bases import BASE, DRONE
import utilities.icon_generator as icon_generator


URL_BASE = "http://localhost:8000/{}/".format(BASE)
DRONE_BASE = "{}{}/".format(URL_BASE, DRONE)
CONN_TYPES = ["Radio", "Ardupilot SIL", "Test"]
BAUD = ["9600", "38400", "56700", "115200"]

ALL_COLORS = icon_generator.COLORS


class ConWindow(QDialog, Ui_MainWindow):
    """Main interface for the connection window."""

    def __init__(self, ctx, ports, used_colors):
        super().__init__()

        self.ctx = ctx
        self.radio_ports = ports
        self.TCP = False
        self.setupUi(self)

        available_colors = [i for i in ALL_COLORS if i not in used_colors]

        self.comboBox_conn_type.addItems(CONN_TYPES)
        self.comboBox_color.addItems(available_colors)
        self.comboBox_port.setEnabled(False)
        self.comboBox_baud.setEnabled(False)
        self.comboBox_baud.addItems(BAUD)

        self.pushButton_connect.clicked.connect(self.clicked_connect)
        self.pushButton_cancel.clicked.connect(self.clicked_cancel)
        self.comboBox_conn_type.currentTextChanged.connect(self.check_conn_type)

    def clicked_cancel(self):
        self.reject()

    def check_conn_type(self):
        conn_type = self.comboBox_conn_type.currentText()

        if conn_type == "Radio":
            self.prepare_elements_dynamically(False, self.radio_ports, True)

        elif conn_type == "Ardupilot SIL":
            self.prepare_elements_dynamically(True, ["tcp:127.0.0.1:"], False)

        elif conn_type == "Test":
            self.prepare_elements_dynamically(False, ["/dev/test/"], False)

    def prepare_elements_dynamically(self, tcp_bool, port_items, baud_bool):
        self.TCP = tcp_bool
        self.comboBox_port.clear()
        self.comboBox_port.addItems(port_items)
        self.lineEdit_extra_tcp.setEnabled(tcp_bool)
        self.comboBox_baud.setEnabled(baud_bool)

    def clicked_connect(self):

        port_name = self.comboBox_port.currentText()
        if self.TCP:
            port_name += str(self.lineEdit_extra_tcp.text())

        self.color_id = self.comboBox_color.currentText()
        self.baud = int(self.comboBox_baud.currentText())
        self.name = self.lineEdit_nameinput.text()

        url = "{}connect".format(DRONE_BASE)

        if len(port_name) > 0 or len(self.name) > 0:
            url += "?"
            added_data = False

            if len(port_name) > 0:
                url += "port=" + port_name.replace("/", "%2F")
                added_data = True

            if len(self.name) > 0:
                if added_data:
                    url += "&"
                url += "name=" + self.name.replace(" ", "_")
                added_data = True

            if len(self.color_id) > 0:
                if added_data:
                    url += "&"
                url += "color=" + self.color_id.replace(" ", "_")
                added_data = True

            if added_data:
                url += "&"
            url += "baud={:d}".format(self.baud)
            added_data = True

        conn = requests.get(url).json()

        msgBox = QMessageBox()

        if conn["success"]:
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Information")
            msgBox.setText("Connected to vehicle: {}".format(self.name))
            msgBox.exec()
            self.accept()

        else:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Warning")
            msgBox.setText("Failed connection: <<{:s}>>".format(conn["msg"]))
            msgBox.exec()

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

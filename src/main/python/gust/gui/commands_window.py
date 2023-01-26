"""Logic for Autopilot Commands Window"""
import requests
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from utilities import ConnSettings as conn_settings
from gust.gui.ui.commands_window import Ui_MainWindow
from wsgi_apps.api.url_bases import BASE, DRONE

URL_BASE = "http://localhost:8000/{}/".format(BASE)
DRONE_BASE = "{}{}/".format(URL_BASE, DRONE)
FLIGHT_MODES = ["STABILIZE", "GUIDED", "AUTO", "RTL"]


class CommandsManager(QMainWindow, Ui_MainWindow):
    """Main Interface for the Autopilot Commands Window"""

    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)

        self.ctx = ctx
        self.setupUi(self)

        # {'name': 'color'}
        self.vehicles = {}
        self.selected_name = None

        self.pushButton_refresh.clicked.connect(self.clicked_refresh)
        self.pushButton_select.clicked.connect(self.clicked_select)
        self.pushButton_mode.clicked.connect(self.clicked_set_mode)
        self.comboBox_mode.addItems(FLIGHT_MODES)

    def clicked_refresh(self):
        url = "{}get_connected_drones_with_color".format(DRONE_BASE)
        self.vehicles = requests.get(url).json()
        self.comboBox_names.addItems(self.vehicles.keys())

    def clicked_select(self):
        self.selected_name = self.comboBox_names.currentText()
        self.label_drone_name.setText(self.selected_name)

    def clicked_do_action(self):
        pass

    def clicked_set_wp(self):
        pass

    def clicked_set_mode(self):
        if self.selected_name is not None:
            sel_mode = self.comboBox_mode.currentText()
            url = "{}autopilot_cmd".format(DRONE_BASE)
            url += "?name=" + self.selected_name.replace(" ", "_")
            url += "&cmd=" + conn_settings.SET_MODE
            url += "&param=" + sel_mode
            print(url)
            set_mode = requests.get(url).json()
            self.show_message_box(set_mode['success'], set_mode['msg'])
        else:
            self.show_message_box(False, "Vehicle not selected")

    def clicked_set_speed(self):
        pass

    def clicked_set_altitude(self):
        pass

    def clicked_arm_disarm(self):
        pass

    def clicked_takeoff(self):
        url = "{}autopilot_cmd".format(DRONE_BASE)
        url += "?name=" + self.selected_name.replace(" ", "_")
        url += "&cmd=" + conn_settings.TAKEOFF
        url += "&param=" + "10"
        takeoff = requests.get(url).json()

        self.show_message_box(takeoff['success'], takeoff['msg'])

    def clicked_goto_next(self):
        pass

    def clicked_restart_mission(self):
        pass

    def clicked_rtl(self):
        pass

    def show_message_box(self, succ, msg):
        if not succ:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(msg)
            msgBox.exec()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

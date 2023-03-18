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
        self.pushButton_arm.clicked.connect(self.clicked_arm)
        self.pushButton_disarm.clicked.connect(self.clicked_disarm)
        self.pushButton_takeoff.clicked.connect(self.clicked_takeoff)
        self.pushButton_goto_next.clicked.connect(self.clicked_goto_next)
        self.pushButton_rtl.clicked.connect(self.clicked_rtl)
        self.comboBox_mode.addItems(FLIGHT_MODES)

    def clicked_refresh(self):
        self.comboBox_names.clear()
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

    def clicked_arm(self):
        if self.selected_name is not None:
            self.send_arm_disarm_request(1)
        else:
            self.show_message_box(False, "Vehicle not selected")

    def clicked_disarm(self):
        if self.selected_name is not None:
            self.send_arm_disarm_request(0)
        else:
            self.show_message_box(False, "Vehicle not selected")

    def send_arm_disarm_request(self, param):
        if self.selected_name is not None:
            url = "{}autopilot_cmd".format(DRONE_BASE)
            url += "?name=" + self.selected_name.replace(" ", "_")
            url += "&cmd=" + conn_settings.ARM_DISARM
            url += "&param=" + str(param)
            arm = requests.get(url).json()
            self.show_message_box(arm["success"], arm["msg"])
        else:
            self.show_message_box(False, "Vehicle not selected")

    def clicked_set_mode(self):
        self.set_flight_mode(self.comboBox_mode.currentText())

    def clicked_rtl(self):
        self.set_flight_mode("RTL")

    def set_flight_mode(self, mode):
        if self.selected_name is not None:
            url = "{}autopilot_cmd".format(DRONE_BASE)
            url += "?name=" + self.selected_name.replace(" ", "_")
            url += "&cmd=" + conn_settings.SET_MODE
            url += "&param=" + mode
            set_mode = requests.get(url).json()
            self.show_message_box(set_mode["success"], set_mode["msg"])
        else:
            self.show_message_box(False, "Vehicle not selected")

    def clicked_set_speed(self):
        pass

    def clicked_set_altitude(self):
        pass

    def clicked_takeoff(self):
        if self.selected_name is not None:
            url = "{}autopilot_cmd".format(DRONE_BASE)
            url += "?name=" + self.selected_name.replace(" ", "_")
            url += "&cmd=" + conn_settings.TAKEOFF
            url += "&param=" + self.lineEdit_takeoff_alt.text()
            takeoff = requests.get(url).json()
            self.show_message_box(takeoff["success"], takeoff["msg"])
        else:
            self.show_message_box(False, "Vehicle not selected")

    def clicked_goto_next(self):
        for name in self.vehicles.keys():
            url = "{}autopilot_cmd".format(DRONE_BASE)
            url += "?name=" + name.replace(" ", "_")
            url += "&cmd=" + conn_settings.GOTO_NEXT_WP
            url += "&param=" + "0"
            goto_next = requests.get(url).json()


        # if self.selected_name is not None:
        #     url = "{}autopilot_cmd".format(DRONE_BASE)
        #     url += "?name=" + self.selected_name.replace(" ", "_")
        #     url += "&cmd=" + conn_settings.GOTO_NEXT_WP
        #     url += "&param=" + "0"
        #     goto_next = requests.get(url).json()
        #     self.show_message_box(goto_next["success"], goto_next["msg"])
        # else:
        #     self.show_message_box(goto_next["success"], goto_next["msg"])

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

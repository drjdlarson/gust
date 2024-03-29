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

        self.vehicles = {}
        self.selected_name = None
        self.selected_cmrA_name = None
        self.selected_cmrB_name = None

        # event connections
        self.pushButton_refresh.clicked.connect(self.clicked_refresh)
        self.pushButton_select.clicked.connect(self.clicked_select)
        self.pushButton_select_cmrA.clicked.connect(self.clicked_select_cmrA)
        self.pushButton_select_cmrB.clicked.connect(self.clicked_select_cmrB)
        self.pushButton_mode.clicked.connect(self.clicked_set_mode)
        self.pushButton_arm.clicked.connect(self.clicked_arm)
        self.pushButton_disarm.clicked.connect(self.clicked_disarm)
        self.pushButton_takeoff.clicked.connect(self.clicked_takeoff)
        self.pushButton_goto_next_single.clicked.connect(self.clicked_goto_next_single)
        self.pushButton_goto_next_cmr.clicked.connect(self.clicked_goto_wp_cmr)
        self.comboBox_mode.addItems(FLIGHT_MODES)

    def clicked_refresh(self):
        """Gets an updated list of vehicles connected"""
        self.comboBox_names.clear()
        url = "{}get_connected_drones_with_color".format(DRONE_BASE)
        self.vehicles = requests.get(url).json()
        self.comboBox_names.addItems(self.vehicles.keys())
        self.comboBox_names_cmrA.addItems(self.vehicles.keys())
        self.comboBox_names_cmrB.addItems(self.vehicles.keys())

    def clicked_select(self):
        """Selects a vehicle from the list of connected vehicles.
        Selected vehicle's name is displayed in the center.
        This step is required before performing any commands for the vehicle"""
        self.selected_name = self.comboBox_names.currentText()
        self.label_drone_name.setText(self.selected_name)

    def clicked_select_cmrA(self):
        """Selects first vehicle for CMR"""
        self.selected_cmrA_name = self.comboBox_names_cmrA.currentText()
        self.label_cmrA_name.setText(self.selected_cmrA_name)

    def clicked_select_cmrB(self):
        """Selects second vehicle for CMR"""
        self.selected_cmrB_name = self.comboBox_names_cmrB.currentText()
        self.label_cmrB_name.setText(self.selected_cmrB_name)

    def clicked_do_action(self):
        pass

    def clicked_set_wp(self):
        pass

    def clicked_arm(self):
        """Arms the selected vehicle"""
        self.send_arm_disarm_request(1)

    def clicked_disarm(self):
        """Disarms the selected vehicle"""
        self.send_arm_disarm_request(0)

    def send_arm_disarm_request(self, param):
        # Check if the selection is not empty
        if self.selected_name is not None:
            # See WSGI App's drone_namespace for further logic
            url = "{}autopilot_cmd".format(DRONE_BASE)
            url += "?name=" + self.selected_name.replace(" ", "_")
            url += "&cmd=" + conn_settings.ARM_DISARM
            url += "&param=" + str(param)
            arm = requests.get(url).json()
            self.show_message_box(arm["success"], arm["msg"])
        else:
            self.show_message_box(False, "Vehicle not selected")

    def clicked_set_mode(self):
        """Changes the flight mode based on the ComboBox selection"""
        self.set_flight_mode(self.comboBox_mode.currentText())

    def set_flight_mode(self, mode):
        # Check if the selection is not empty
        if self.selected_name is not None:
            # See WSGI App's drone_namespace for further logic
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
        # Check if the selection is not empty
        if self.selected_name is not None:
            # See WSGI App's drone_namespace for further logic
            url = "{}autopilot_cmd".format(DRONE_BASE)
            url += "?name=" + self.selected_name.replace(" ", "_")
            url += "&cmd=" + conn_settings.TAKEOFF

            if self.lineEdit_takeoff_alt.text() is not None:
                takeoff_alt = self.lineEdit_takeoff_alt.text()
            # set take-off alt to 50m if no altitude is provided
            else:
                takeoff_alt = 50

            url += "&param=" + takeoff_alt
            takeoff = requests.get(url).json()
            self.show_message_box(takeoff["success"], takeoff["msg"])
        else:
            self.show_message_box(False, "Vehicle not selected")

    def clicked_goto_next_single(self):
        """Commands the current vehicle to proceed to the next waypoint."""

        url = "{}autopilot_cmd".format(DRONE_BASE)
        url += "?name=" + self.selected_name.replace(" ", "_")
        url += "&cmd=" + conn_settings.GOTO_NEXT_WP
        url += "&param=" + self.spinBox_next_wp.value()
        goto_next = requests.get(url).json()

        # Check if the selection is not empty
        # if self.selected_name is not None:
        #     See WSGI App's drone_namespace for further logic
        #     url = "{}autopilot_cmd".format(DRONE_BASE)
        #     url += "?name=" + self.selected_name.replace(" ", "_")
        #     url += "&cmd=" + conn_settings.GOTO_NEXT_WP
        #     url += "&param=" + "0"
        #     goto_next = requests.get(url).json()
        #     self.show_message_box(goto_next["success"], goto_next["msg"])
        # else:
        #     self.show_message_box(goto_next["success"], goto_next["msg"])

    def clicked_goto_wp_cmr(self):
        """Commands both selected CMR vehicles to proceed to the given waypoint"""
        cmr_wp = [
            self.spinBox_cmrA_wp.value(),
            self.spinBox_cmrB_wp.value(),
        ]
        # Send the wp command for both vehicles
        for index, name in enumerate(
            [self.selected_cmrA_name, self.selected_cmrB_name]
        ):
            url = "{}autopilot_cmd".format(DRONE_BASE)
            url += "?name=" + name.replace(" ", "_")
            url += "&cmd=" + conn_settings.GOTO_NEXT_WP
            url += "&param=" + str(cmr_wp[index])
            goto_wp = requests.get(url).json()

    def clicked_restart_mission(self):
        pass

    def show_message_box(self, succ, msg):
        """Displays the messages in a separate dialogue box"""
        if not succ:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(msg)
            msgBox.exec()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

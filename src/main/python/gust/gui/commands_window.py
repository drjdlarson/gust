"""Logic for Autopilot Commands Window"""
import requests
from PyQt5.QtWidgets import QMainWindow

from utilities import ConnSettings as conn_settings
from gust.gui.ui.commands_window import Ui_MainWindow
from wsgi_apps.api.url_bases import BASE, DRONE

URL_BASE = "http://localhost:8000/{}/".format(BASE)
DRONE_BASE = "{}{}/".format(URL_BASE, DRONE)
FLIGHT_MODES = ['STABILIZE', 'GUIDED', 'AUTO', 'RTL']

class CommandsManager(QMainWindow, Ui_MainWindow):
    """Main Interface for the Autopilot Commands Window"""

    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)

        self.ctx = ctx

        self.names = []
        self.selected = None

        self.pushButton_refresh.clicked.connect(self.clicked_refresh)
        self.pushButton_select.clicked.connect(self.clicked_select)
        self.comboBox_mode.addItems(FLIGHT_MODES)

    def clicked_refresh(self):
        url = "{}get_connected_drones_with_color".format(DRONE_BASE)
        self.names = requests.get(url).json()
        self.comboBox_refresh.addItems(self.names)

    def clicked_select(self):
        self.selected = self.comboBox_names.currentText()
        self.label_drone_name.setText(self.selected)

    def clicked_do_action(self):
        pass

    def clicked_set_wp(self):
        pass

    def clicked_set_mode(self):
        pass

    def clicked_set_speed(self):
        pass

    def clicked_set_altitude(self):
        pass

    def clicked_arm_disarm(self):
        pass

    def clicked_takeoff(self):
        url = "{}autopilot_cmd"
        url += "?name=" + self.selected.replace(' ', '_')
        url += "&cmd=" + conn_settings.TAKEOFF
        url += "&param=" + "10"
        takeoff = requests.get(url).json()

    def clicked_goto_next(self):
        pass

    def clicked_restart_mission(self):
        pass

    def clicked_rtl(self):
        pass



    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

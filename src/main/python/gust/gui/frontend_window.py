"""Logic for main frontend window."""
import time
from datetime import timedelta
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QPushButton,
)
from PyQt5.QtCore import (
    pyqtSlot,
    pyqtSignal,
    QTimer,
)
import requests
import gust.gui.msg_decoder as msg_decoder
from gust.gui.ui.gustClient import Ui_MainWindow_main
from gust.gui import (
    con_window,
    sensors_window,
    planning_selection_window,
    commands_window,
    start_sil_window,
)
from gust.gui import (
    engineoff_confirmation,
    disconnect_confirmation,
    rtl_confirmation,
    disarm_confirmation,
)
from wsgi_apps.api.url_bases import BASE, DRONE


URL_BASE = "http://localhost:8000/{}/".format(BASE)
DRONE_BASE = "{}{}/".format(URL_BASE, DRONE)
FILES = ["home", "pos", "spos", "rtl_pos"]

# front-end update rate in Hz.
_FE_UPDATE_RATE = 12


class FrontendWindow(QMainWindow, Ui_MainWindow_main):
    """Main interface for the frontend window."""

    def __init__(self, ctx):
        super().__init__()
        self.timer = None

        # instances of each external dialog window
        self._conWindow = None
        self._sensorsWindow = None
        self._cmdWindow = None
        self._servoWindow = None
        self._planningWindow = None
        self._sil_window = None

        self.sil_vehicles = []
        self._continue_updating_data = False
        self.flight_params = None

        self.manager = DataManager()
        self.ctx = ctx
        self.setupUi(self)

        # event connections
        self.pushButton_addvehicle.clicked.connect(self.clicked_addvehicle)
        self.pushButton_sil.clicked.connect(self.clicked_sil)

        self.pushButton_engineOff.clicked.connect(self.clicked_engineOff)
        self.pushButton_RTL.clicked.connect(self.clicked_RTL)
        self.pushButton_disarm.clicked.connect(self.clicked_disarm)

        self.pushButton_refresh_map.clicked.connect(self.clicked_refresh_map)
        self.pushButton_sensors.clicked.connect(self.clicked_sensors)
        self.pushButton_commands.clicked.connect(self.clicked_commands)
        self.pushButton_tune.clicked.connect(self.clicked_tune)
        self.pushButton_sensors.clicked.connect(self.clicked_sil)
        self.pushButton_planning.clicked.connect(self.clicked_planning)

        self.comboBox_saved_locations.currentTextChanged.connect(self.recenter_map)

        self.once_clicked = False
        self.tableWidget.cellClicked.connect(self.item_clicked)

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)
        self.widget_map.setup_qml(self.ctx)
        self.widget_hud.setup_hud_ui(self.ctx)

        # saved locations information is stored in gust/src/main/resources/base
        # can add more locations for new places
        url = "{}get_saved_locations".format(DRONE_BASE)
        self.saved_locations = requests.get(url).json()
        self.comboBox_saved_locations.addItems(self.saved_locations.keys())

    def recenter_map(self):
        """Recenter the QML Map"""
        center_location = self.comboBox_saved_locations.currentText()
        center_coords = self.saved_locations[center_location]
        self.widget_map.recenter_map(center_coords)

    @pyqtSlot()
    def clicked_addvehicle(self):
        """Opens the ConWindow to connect a vehicle"""
        url = "{}get_available_ports".format(DRONE_BASE)
        ports = requests.get(url).json()

        url = "{}get_used_colors".format(DRONE_BASE)
        used_colors = requests.get(url).json()

        # Creating an instance of ConWindow class.
        if self._conWindow is None:
            self._conWindow = con_window.ConWindow(
                self.ctx, ports["ports"], used_colors["used_colors"], self.sil_vehicles
            )

        # Once connection is successful from ConWindow
        if self._conWindow.exec_():
            time.sleep(2.0)
            self._continue_updating_data = True

            # adding a row in the table and starting data request
            rowPos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPos)
            self.update_request()
        # remove the ConWindow instance
        self._conWindow = None

    @pyqtSlot()
    def clicked_engineOff(self):
        """Opens the EngineOffConfirmation to connect a vehicle"""
        win = engineoff_confirmation.EngineOffConfirmation(self.ctx)
        win.exec_()

    @pyqtSlot()
    def clicked_RTL(self):
        """Opens the RTLConfirmation to connect a vehicle"""
        win = rtl_confirmation.RTLConfirmation(self.ctx)
        win.exec_()

    @pyqtSlot()
    def clicked_disarm(self):
        """Opens the DisarmConfirmation to connect a vehicle"""
        win = disarm_confirmation.DisarmConfirmation(self.ctx)
        win.exec_()

    @pyqtSlot()
    def clicked_tune(self):
        """Currently not supported"""
        pass

    @pyqtSlot()
    def clicked_sensors(self):
        """Opens the SensorWindow"""
        if self._sensorsWindow is None:
            self._sensorsWindow = sensors_window.SensorsWindow(self.ctx, parent=self)
        self._sensorsWindow.show()

    def clicked_sil(self):
        """Opens the StartSILWindow for starting a new Ardupilot SIL"""
        if self._sil_window is None:
            self._sil_window = start_sil_window.StartSILWindow(
                self.ctx, self.saved_locations
            )
            # signal is emiited from _sil_window once SIL is started successfully
            self._sil_window.signal.connect(self.add_sil_vehicle)

        self._sil_window.exec_()
        self._sil_window = None

    @pyqtSlot()
    def clicked_planning(self):
        """Opens the PlanningSelectionWindow"""
        if self._planningWindow is None:
            self._planningWindow = planning_selection_window.PlanningSelectionWindow(
                self.ctx, parent=self
            )
        self._planningWindow.show()
        self._planningWindow = None

    @pyqtSlot()
    def clicked_commands(self):
        """Opens the CommandsManager"""
        if self._cmdWindow is None:
            self._cmdWindow = commands_window.CommandsManager(self.ctx, parent=self)
        self._cmdWindow.show()

    @pyqtSlot()
    def clicked_disconnect(self):
        """Sends a disconnect request for a vehicle selected"""

        # Finding the name of the vehicle to disconnect
        button = self.sender()
        if button:
            sel_row = self.tableWidget.indexAt(button.pos()).row()
            name = self.tableWidget.item(sel_row, 1).text()
            win = disconnect_confirmation.DisconnectConfirmation(name, self.ctx)
            res = win.exec_()

            # res represents the response of the disonnect_confirmation dialog window
            if res:
                # remove the vehicle's row from the table
                self.tableWidget.removeRow(sel_row)

                # if it was a SIL vehicle, remove its name from this list.
                if name in self.sil_vehicles:
                    self.sil_vehicles.remove(name)

                # keep continuing data updates if there is at least one vehicle connected on the table
                self._continue_updating_data = self.tableWidget.rowCount() > 0
                self.clean_hud_and_lcd()
                print("vehicle disconnecting is {}".format(name))
                self.widget_map.remove_vehicle_from_map(name)

    def add_sil_vehicle(self, sil_name):
        """
        Adds sil_name to the list of SIL vehicles

        Parameters
        ----------
        sil_name: str
            Name of the SIL vehicle
        Returns
        -------

        """
        self.sil_vehicles.append(sil_name)

    def update_request(self):
        """Starts the data update requests"""

        if self.timer is None:
            self.timer = QTimer()
            self.manager.timer = self.timer
            self.manager.rate = (1 / _FE_UPDATE_RATE) * 1000

            # run the requests at a certain interval
            self.timer.timeout.connect(self.manager.run)

            # update the UI everytime data is received from the requests
            self.manager.signal.connect(self.update_frame)
            if self._continue_updating_data:
                self.timer.start(self.manager.rate)

    def update_frame(self, passed_signal):
        """
        Receives the messages from DataManager and populates the UI

        Parameters
        ----------
        passed_signal: dict
            Messages from DanaManager. The dict is defined in WSGI Apps

        Returns
        -------

        """
        self.flight_params = passed_signal

        # populating the table
        for key in self.flight_params:
            rowPos = int(key) - 1

            item = QTableWidgetItem()
            color = self.flight_params[key]["color"]
            item.setBackground(QtGui.QColor(color))
            self.tableWidget.setItem(rowPos, 0, item)

            item = self.flight_params[key]["name"]
            item = QTableWidgetItem(item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 1, item)

            item = self.flight_params[key]["flight_mode"]
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 2, item)

            item = self.flight_params[key]["next_wp"]
            item = QTableWidgetItem("Waypoint " + str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 3, item)

            item = int(self.flight_params[key]["tof"])
            item = QTableWidgetItem(str(timedelta(seconds=item)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 4, item)

            item = self.flight_params[key]["relative_alt"]
            item = QTableWidgetItem(str(item) + " m")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 5, item)

            item = self.flight_params[key]["voltage"]
            item = QTableWidgetItem(str(item) + " V")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 6, item)

            item = self.flight_params[key]["current"]
            item = QTableWidgetItem(str(item) + " A")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 7, item)

            item = self.flight_params[key]["relay_sw"]
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 8, item)

            item = self.flight_params[key]["engine_sw"]
            item = QTableWidgetItem(str(item))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPos, 9, item)

            # self.con_status will be 1 or 0.
            self.disconnect_button = QPushButton("Disconnect")
            self.disconnect_button.clicked.connect(self.clicked_disconnect)
            self.tableWidget.setCellWidget(rowPos, 10, self.disconnect_button)

            # send all info for each vehicle to the MapWidget
            self.widget_map.add_drone(
                self.flight_params[key]["name"],
                self.flight_params[key]["color"],
                self.flight_params[key]["home_lat"],
                self.flight_params[key]["home_lon"],
                self.flight_params[key]["latitude"],
                self.flight_params[key]["longitude"],
                self.flight_params[key]["yaw"],
                self.flight_params[key]["heading"],
                self.flight_params[key]["flight_mode"],
            )

        if self.once_clicked:
            self.vehicle_selected()

    def item_clicked(self, row):
        """
        Actions to perform when an item is clicked on the table

        Parameters
        ----------
        row: int
            row of cell clicked on the table

        Returns
        -------

        """
        self.once_clicked = True
        self.row = row
        self.vehicle_selected()

    def vehicle_selected(self):
        """Displays the parameters for the selected vehicle on the left pane"""
        key_val = self.row
        key_val += 1
        key_pos = str(key_val)

        # Updating the Labels
        self.label_seluav.setText(str(self.flight_params[key_pos]["name"]).upper())
        vehicle_type = msg_decoder.MessageDecoder.findType(
            self.flight_params[key_pos]["vehicle_type"]
        )
        self.label_vehicle_type.setText(vehicle_type)
        self.label_status.setText(str(self.flight_params[key_pos]["sys_status"]))

        # setting ekf status
        if bool(self.flight_params[key_pos]["ekf_ok"]):
            ekf_str = "EKF_GOOD"
        else:
            ekf_str = "EKF_BAD"
        self.label_ekf.setText(ekf_str)

        # Updating the LCD display
        self.lcdNumber_altitude.display(self.flight_params[key_pos]["relative_alt"])
        self.lcdNumber_vspeed.display(self.flight_params[key_pos]["vspeed"])
        self.lcdNumber_airspeed.display(self.flight_params[key_pos]["airspeed"])
        self.lcdNumber_heading.display(self.flight_params[key_pos]["yaw"])
        self.lcdNumber_voltage.display(self.flight_params[key_pos]["voltage"])
        self.lcdNumber_current.display(self.flight_params[key_pos]["current"])

        # Updating the Attitude Indicator
        self.widget_hud.roll_angle = self.flight_params[key_pos]["roll_angle"]
        self.widget_hud.pitch_angle = self.flight_params[key_pos]["pitch_angle"]
        self.widget_hud.gndspeed = self.flight_params[key_pos]["gndspeed"]
        self.widget_hud.airspeed = self.flight_params[key_pos]["airspeed"]
        self.widget_hud.altitude = self.flight_params[key_pos]["relative_alt"]
        self.widget_hud.vspeed = self.flight_params[key_pos]["vspeed"]
        self.widget_hud.yaw = self.flight_params[key_pos]["yaw"]
        self.widget_hud.arm = self.flight_params[key_pos]["armed"]
        self.widget_hud.gnss_fix = self.flight_params[key_pos]["gnss_fix"]
        self.widget_hud.mode = self.flight_params[key_pos]["flight_mode"]
        self.widget_hud.alpha = self.flight_params[key_pos]["alpha"]
        self.widget_hud.beta = self.flight_params[key_pos]["beta"]
        self.widget_hud.sat_count = self.flight_params[key_pos]["satellites_visible"]
        self.widget_hud.repaint()

    def clicked_refresh_map(self):
        """Re-centers the map and display the uploaded waypoints from all vehicles"""

        # Need to implement this
        # self.recenter_map()
        if self.flight_params is not None:
            if len(self.flight_params) != 0:
                # request uploaded waypoints from the vehicles
                url = "{}download_wp".format(DRONE_BASE)
                all_waypoints = requests.get(url).json()

                # display the waypoints on the map
                self.widget_map.display_missions(all_waypoints)

    def clean_hud_and_lcd(self):
        """Cleaning the LCD display and HUD"""
        self.label_seluav.setText("VEHICLE NAME")
        self.label_status.setText("SYSTEM STATUS")
        self.label_ekf.setText("EKF STATUS")
        self.label_vehicle_type.setText("VEHICLE TYPE")

        self.lcdNumber_altitude.display(0)
        self.lcdNumber_vspeed.display(0)
        self.lcdNumber_airspeed.display(0)
        self.lcdNumber_heading.display(0)
        self.lcdNumber_voltage.display(0)
        self.lcdNumber_current.display(0)

        self.widget_hud.clean_hud()
        self.tableWidget.clearContents()


class DataManager(QtCore.QObject):
    # signal to notify FrontendWindow once a set of data is received and packaged as dict
    signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.rate = None
        self.timer = None
        self.vehicles_list = {}

    @pyqtSlot()
    def run(self):
        """
        This function is called at a certain interval. See update_request() method of FrontendWindow.
        It sends http requests to the WSGI App to receive messages.
        It emits 'signal' whenever the messages are received.
        The 'signal' is used by FrontendWindow to display information.

        Returns
        -------

        """

        # The signal is packaged as a dict vehicles_list.
        # vehicle_list = {1: {'voltage':48, 'current'=16, ...}, 2: {....}}

        self.vehicles_list = {}

        url = "{}sys_data".format(DRONE_BASE)
        sys_data = requests.get(url).json()

        url = "{}attitude_data".format(DRONE_BASE)
        attitude_data = requests.get(url).json()

        url = "{}pos_data".format(DRONE_BASE)
        pos_data = requests.get(url).json()

        url = "{}sys_info".format(DRONE_BASE)
        sys_info = requests.get(url).json()

        all_signals = [sys_data, attitude_data, pos_data, sys_info]

        # package the messages nicely
        for item in all_signals:
            for key, values in item.items():
                if key not in self.vehicles_list:
                    self.vehicles_list[key] = values
                self.vehicles_list[key].update(values)

        # emit the signal. this signal is caught by FrontendWindow.update_request()
        self.signal.emit(self.vehicles_list)

        # restart the timer
        self.timer.start(self.rate)

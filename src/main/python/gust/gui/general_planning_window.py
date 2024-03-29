"""Logic for General Planning Window"""

import requests
import random
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (
    QMainWindow,
    QCheckBox,
    QMessageBox,
    QFileDialog,
    QTableWidgetItem,
    QPushButton,
    QComboBox,
)
from utilities import ConnSettings as conn_settings
from gust.gui.ui.general_planning import Ui_MainWindow
from wsgi_apps.api.url_bases import BASE, DRONE
from gust.gui.ui.map_widget import MapHelper

URL_BASE = "http://localhost:8000/{}/".format(BASE)
DRONE_BASE = "{}{}/".format(URL_BASE, DRONE)
FILES = ["home", "pos", "spos", "rtl_pos"]

# picked up random colors from QML colors type
# https://doc.qt.io/qt-6/qml-color.html
ALL_COLORS = [
    "aqua",
    "yellow",
    "blue",
    "darkcyan",
    "darkorange",
    "red",
    "green",
    "sienna",
    "darkslateblue",
    "fuchsia",
]


class GeneralPlanningWindow(QMainWindow, Ui_MainWindow):
    """Main Interface for general planning window."""

    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)

        self.ctx = ctx
        self.setupUi(self)
        self.loaded_mission_wps = {}
        self.file_names = {}
        self.mission_colors = {}
        self.cb = {}

        # event connections
        self.pushButton_load_file.clicked.connect(self.clicked_load_file)
        self.pushButton_refresh.clicked.connect(self.clicked_refresh)
        self.tableWidget_missions.cellClicked.connect(self.item_clicked_on_table)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)

        self.widget_planning_map.setup_qml(self.ctx)

    def clicked_load_file(self):
        """Open a dialog window to select the mission file and populate."""

        # setting up the dialog window to select mission file
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.setNameFilter("Waypoints (*.txt *.waypoints)")
        dlg.setViewMode(QFileDialog.List)

        # Once a file is selected
        if dlg.exec_():
            fnames = dlg.selectedFiles()

            # For each selected file
            for fname in fnames:
                self.load_mission_file(fname)

    def load_mission_file(self, filename):
        """Tasks to perform when a mission file is loaded"""

        # getting the file name excluding the full path and extension name
        mission_name = (filename.split("/")[-1]).split(".")[0]

        # Avoid missions with duplicate names
        if mission_name not in self.loaded_mission_wps.keys():
            # saving the filepath (required to send it to ConnServer.)
            self.file_names[mission_name] = filename

            # assign a color to the loaded mission
            self.mission_colors[mission_name] = self.assign_color_to_the_mission(
                mission_name
            )

            # reading the XYZ and command from the file.
            self.loaded_mission_wps[mission_name] = self.read_pos_from_file(filename)

            # populating the missions table
            self.add_row_in_missions(mission_name)

            # add the mission to the map
            self.add_mission_to_map(mission_name)

            # add checkboxes for map visibility
            self.add_checkbox_for_mission(mission_name)

        else:
            msg = "{} name already exists".format(mission_name)
            self.display_message(QMessageBox.Warning, msg)

    def add_checkbox_for_mission(self, mission):
        """Add Checkbox for each mission to change visibility in the map"""

        self.cb[mission] = QCheckBox(mission)
        self.cb[mission].setTristate(True)
        self.cb[mission].setCheckState(True)
        self.cb[mission].stateChanged.connect(self.checkbox_state_changed)
        self.horizontalLayout_checkboxes.addWidget(self.cb[mission])

    @pyqtSlot()
    def checkbox_state_changed(self):
        """Hide or display the waypoints for selected mission"""

        sel_checkbox_object = self.sender()
        # finding the mission name using checkbox' name
        sel_wp_color = self.mission_colors[sel_checkbox_object.text()]

        # change the state
        if sel_checkbox_object.isChecked():
            self.widget_planning_map.change_waypoints_line_state(1, sel_wp_color)
        else:
            self.widget_planning_map.change_waypoints_line_state(0, sel_wp_color)

    def add_mission_to_map(self, mission):
        """Displays the loaded mission on the map"""

        # Only picking the (X, Y) values
        coords = [
            self.loaded_mission_wps[mission][index][:2]
            for index in range(len((self.loaded_mission_wps[mission])))
        ]

        # Remove the waypoints with (x,y) == (0.0, 0.0), (1,0, 1.0) from showing in map
        coordinates = MapHelper.remove_coord_from_wplist(
            coords, [(0.0, 0.0), (1.0, 1.0)]
        )

        # display on the map
        self.widget_planning_map.add_waypoint_lines(
            coordinates, self.mission_colors[mission]
        )

    def assign_color_to_the_mission(self, mission_name):
        """Assigns a color to the loaded mission"""
        available_colors = [
            i for i in ALL_COLORS if i not in self.mission_colors.values()
        ]
        return random.choice(available_colors)

    def add_row_in_missions(self, mission):
        """Adding the new mission name in the table"""

        # Adding the new row.
        rowPos = self.tableWidget_missions.rowCount()
        self.tableWidget_missions.insertRow(rowPos)

        # First column: Mission name
        item = QTableWidgetItem(mission)
        item.setBackground(QtGui.QColor(self.mission_colors[mission]))
        self.tableWidget_missions.setItem(rowPos, 0, item)

        # Second column: dropdown for vehicle selection
        vehicle_dropdown = QComboBox()
        self.tableWidget_missions.setCellWidget(rowPos, 1, vehicle_dropdown)

        # Third Column: button to upload
        upload_button = QPushButton("Upload")
        upload_button.clicked.connect(self.mission_upload)
        self.tableWidget_missions.setCellWidget(rowPos, 2, upload_button)

        # Fourth Column: button to remove that mission
        remove_button = QPushButton("X")
        remove_button.clicked.connect(self.remove_mission)
        self.tableWidget_missions.setCellWidget(rowPos, 3, remove_button)

    def read_pos_from_file(self, file_name):
        """
        Read the mission file and save positions in the loaded_mission_names dict.

        Parameters
        ----------
        file_name : str
            File path for the mission file

        Returns
        -------
        wps : list
            List of tuples containing (X, Y, Z, MAV_CMD)
        """
        wps = []
        with open(file_name) as f:
            for i, line in enumerate(f):
                if i == 0:
                    # Make sure the waypoint file has the correct format
                    if not line.startswith("QGC WPL 110"):
                        raise Exception("Mission is not supported WP version.")
                else:
                    linearray = line.split("\t")
                    ln_x = float(linearray[8])
                    ln_y = float(linearray[9])
                    ln_z = float(linearray[10])
                    ln_command = int(linearray[3])
                    wps.append((ln_x, ln_y, ln_z, ln_command))
        return wps

    @pyqtSlot()
    def mission_upload(self):
        """Uploads the mission to the selected row."""

        # finding the button object that was clicked
        upload_button = self.sender()

        if upload_button:
            sel_row = self.tableWidget_missions.indexAt(upload_button.pos()).row()
            sel_vehicle_name = self.tableWidget_missions.cellWidget(
                sel_row, 1
            ).currentText()
            sel_mission_name = self.tableWidget_missions.item(sel_row, 0).text()

            print("uploading {} to {}".format(sel_mission_name, sel_vehicle_name))

            # Vehicle Name
            url = "{}upload_wp".format(DRONE_BASE)
            url += "?name=" + sel_vehicle_name.replace(" ", "_")

            url += "&filename=" + self.file_names[sel_mission_name]
            url += "&mission_type=" + conn_settings.GEN

            upload = requests.get(url).json()

            if upload["success"]:
                msg = "Uploaded {} waypoints to {}".format(
                    sel_mission_name, sel_vehicle_name
                )
                self.display_message(QMessageBox.Information, msg)
            else:
                msg = "Unable to upload {} waypoints to {}:: {:s}".format(
                    sel_mission_name, sel_vehicle_name, upload["msg"]
                )
                self.display_message(QMessageBox.Warning, msg)

    @pyqtSlot()
    def remove_mission(self):
        """Removes the mission from the list"""
        remove_button = self.sender()

        if remove_button:
            # find the row from which the button was clicked and remove that
            selected_row = self.tableWidget_missions.indexAt(remove_button.pos()).row()
            discon_name = self.tableWidget_missions.item(selected_row, 0).text()
            self.tableWidget_missions.removeRow(selected_row)

            # removing checkboxes
            self.horizontalLayout_checkboxes.removeWidget(self.cb[discon_name])

            # Just delete everything from the table
            self.tableWidget_waypoints.setRowCount(0)

            # delete mission from the map
            self.widget_planning_map.remove_line_from_map(
                self.mission_colors[discon_name]
            )

            # delete other saved stuff.
            del self.loaded_mission_wps[discon_name]
            del self.mission_colors[discon_name]
            del self.file_names[discon_name]
            self.cb[discon_name] = None

    def get_connected_vehicles(self):
        """Find a list of currently connected vehicles."""
        url = "{}get_connected_drones_with_color".format(DRONE_BASE)
        return requests.get(url).json()

    def item_clicked_on_table(self, row):
        """Event connection when any cell is clicked on the missions table"""

        # Clear the table first
        self.tableWidget_waypoints.setRowCount(0)

        # finding the name of selected vehicle. Row is passed by the event connection.
        selected_mission = self.tableWidget_missions.item(row, 0).text()

        for wp in self.loaded_mission_wps[selected_mission]:
            current_rows = self.tableWidget_waypoints.rowCount()
            self.tableWidget_waypoints.insertRow(current_rows)

            # Writing the x-pos (longitude)
            item = QTableWidgetItem(str(wp[0]))
            self.tableWidget_waypoints.setItem(current_rows, 0, item)

            # Writing the y-pos (latitude)
            item = QTableWidgetItem(str(wp[1]))
            self.tableWidget_waypoints.setItem(current_rows, 1, item)

            # Writing the z-pos (altitude)
            item = QTableWidgetItem(str(wp[2]))
            self.tableWidget_waypoints.setItem(current_rows, 2, item)

            # Writing the command: MAV_CMD
            # https://mavlink.io/en/messages/common.html#mav_commands
            item = QTableWidgetItem(str(wp[3]))
            self.tableWidget_waypoints.setItem(current_rows, 3, item)

    def clicked_refresh(self):
        """Event connection when the refresh button is clicked"""

        # Request the list of connected vehicles.
        connected_vehicles = self.get_connected_vehicles()

        # Show the connected vehicles in all dropdowns.
        for row_num in range(self.tableWidget_missions.rowCount()):
            self.tableWidget_missions.cellWidget(row_num, 1).clear()
            self.tableWidget_missions.cellWidget(row_num, 1).addItems(
                connected_vehicles
            )

    def display_message(self, type, msg):
        """Display the message on a separate box"""
        msgBox = QMessageBox()
        msgBox.setIcon(type)
        msgBox.setText(msg)
        msgBox.exec()

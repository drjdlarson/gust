"""Logic for CMR planning window"""
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QCheckBox,
    QTableWidgetItem,
    QPushButton,
    QComboBox,
)
from PyQt5.QtCore import (
    QAbstractListModel,
    Qt,
    QByteArray,
    QProcess,
    QProcessEnvironment,
)
import math
import os
import platform
import logging
import pathlib
import requests
import dronekit
import utilities.database as database
from utilities import ConnSettings as conn_settings
from gust.gui.ui.cmr_window import Ui_MainWindow
from wsgi_apps.api.url_bases import BASE, DRONE


d2r = math.pi / 180
r2d = 1 / d2r
URL_BASE = "http://localhost:8000/{}/".format(BASE)
DRONE_BASE = "{}{}/".format(URL_BASE, DRONE)

_CMR_RUNNING = False

logger = logging.getLogger("[cmr-operation]")


class CmrWindow(QMainWindow, Ui_MainWindow):
    """Main interface for the CMR Planning window."""

    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)

        self.ctx = ctx
        self.setupUi(self)
        self.all_vehicles = {}
        self.cmr_vehicles = []

        self.pushButton_draw_grid.clicked.connect(self.clicked_draw_grid)
        self.pushButton_generate_wp.clicked.connect(
            self.clicked_generate_waypoints
        )
        self.pushButton_load_wp.clicked.connect(
            self.clicked_load_waypoints
        )
        self.checkBox_grid.stateChanged.connect(self.grid_checkbox_changed)
        self.checkBox_waypoints.stateChanged.connect(
            self.waypoints_checkbox_changed
        )
        self.pushButton_refresh.clicked.connect(self.clicked_refresh)
        self.pushButton_start_cmr.clicked.connect(
            self.clicked_start_cmr_operation
        )
        self.pushButton_stop_cmr.clicked.connect(
            self.clicked_stop_cmr_operation
        )


    def clicked_start_cmr_operation(self):
        global _CMR_RUNNING

        if _CMR_RUNNING:
            succ = False
            error = "CMR process already running"

        else:
            if len(self.cmr_vehicles) >= 2:
                url = "{}start_cmr_proc".format(DRONE_BASE)
                cmr_start = requests.get(url).json()
                succ = cmr_start["success"]
                error = cmr_start["msg"]
            else:
                succ = False
                error = (
                    "Cannot start CMR process with less than 2 vehicles"
                )
        msgBox = QMessageBox()
        if succ:
            _CMR_RUNNING = True
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Starting CMR Process")
            msgBox.exec()
        else:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(error)
            msgBox.exec()

    def clicked_stop_cmr_operation(self):
        global _CMR_RUNNING

        if not _CMR_RUNNING:
            succ = False
            error = "CMR Process is not running"
        else:
            url = "{}stop_cmr_proc".format(DRONE_BASE)
            cmr_stop = requests.get(url).json()
            succ = cmr_stop["success"]
            error = cmr_stop["msg"]

        msgBox = QMessageBox()
        if succ:
            _CMR_RUNNING = False
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("CMR Process is stopped")
            msgBox.exec()
        else:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(error)
            msgBox.exec()

    def clicked_refresh(self):
        url = "{}get_connected_drones_with_color".format(DRONE_BASE)
        self.all_vehicles = requests.get(url).json()
        self.populate_drone_table()

    def populate_drone_table(self):
        for name, drone_color in self.all_vehicles.items():
            index = list(self.all_vehicles.keys()).index(name)

            item = QTableWidgetItem()
            item.setBackground(QtGui.QColor(drone_color))
            self.tableWidget_drones.setItem(index, 0, item)

            item = QTableWidgetItem(name)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_drones.setItem(index, 1, item)

            self.comboBox_wp_selection = QComboBox()
            self.comboBox_wp_selection.addItems(self.wp_colors)
            self.tableWidget_drones.setCellWidget(
                index, 2, self.comboBox_wp_selection
            )

            self.upload_button = QPushButton("Upload")
            self.upload_button.clicked.connect(
                self.clicked_upload_waypoints
            )
            self.tableWidget_drones.setCellWidget(
                index, 3, self.upload_button
            )

    def clicked_upload_waypoints(self):
        button = self.sender()
        if button:
            sel_row = self.tableWidget_drones.indexAt(button.pos()).row()
            drone_name = self.tableWidget_drones.item(sel_row, 1).text()
            wp_color = self.tableWidget_drones.cellWidget(
                sel_row, 2
            ).currentText()

            url = "{}upload_wp".format(DRONE_BASE)
            url += "?name=" + drone_name.replace(" ", "_")

            name = "{}_waypoints.txt".format(wp_color)
            rsrc_file = self.ctx.get_resource("cmr_planning/README")
            rsrc_path = str(pathlib.Path(rsrc_file).parent.resolve())
            filename = rsrc_path + "/" + name

            url += "&filename=" + filename
            url += "&mission_type=" + conn_settings.CMR
            url += "&wp_color=" + wp_color

            upload = requests.get(url).json()

            msgBox = QMessageBox()

            if upload["success"]:
                self.cmr_vehicles.append(drone_name)
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText(
                    "Uploaded {} waypoints to {}".format(
                        wp_color, drone_name
                    )
                )
                msgBox.exec()

            else:
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText(
                    "Unable to upload {} waypoints to {}:: {:s}".format(
                        wp_color, drone_name, upload["msg"]
                    )
                )
                msgBox.exec()

    def clicked_test_goto_next(self):
        pass

    # FOR TESTING
    def clicked_load_waypoints(self):
        pass

    def clicked_generate_waypoints(self):
        self.H = float(self.lineEdit_rel_height.text())
        self.s = float(self.lineEdit_spacing.text())
        self.theta_max = float(self.lineEdit_theta_max.text())
        self.theta_min = float(self.lineEdit_theta_min.text())

        self.waypoints = {}
        self.wp_colors = ["red", "blue"]

        # one side of the survey line
        wp1 = self.calculate_waypoints_S(1)

        # other side of the survey line
        wp2 = self.calculate_waypoints_S(-1)

        self.waypoints.update({1: {"coordinates": wp2, "color": "red"}})
        self.waypoints.update({2: {"coordinates": wp1, "color": "blue"}})

        self.write_waypoints_to_a_file(self.waypoints)
        self.widget_cmr_map.add_waypoint_lines(wp1, "blue")
        self.widget_cmr_map.add_waypoint_lines(wp2, "red")
        self.checkBox_waypoints.setCheckState(True)

    def write_waypoints_to_a_file(self, waypoints):
        """
        Writes two waypoint files.
        Compatible to use with MP and QGC

        Parameters
        ----------
        waypoints : dict
            keys: index for drone
            values: list of coordinates and color code of waypoint

        Returns
        -------
        None.

        """
        for key, value in waypoints.items():
            name = "{}_waypoints.txt".format(value["color"])
            list_of_waypoints = value["coordinates"]

            rsrc_file = self.ctx.get_resource("cmr_planning/README")
            rsrc_path = str(pathlib.Path(rsrc_file).parent.resolve())
            filename = rsrc_path + "/" + name
            if os.path.exists(filename):
                os.remove(filename)
            with open(filename, "w") as f:
                f.write("QGC WPL 110\n")
                # manually writing the first line.
                f.write("0\t1\t0\t16\t0\t0\t0.0\t0.0\t1.0\t1.0\t0.0\t1\n")
                for index, tup in enumerate(list_of_waypoints):
                    seq = 2 * index + 1
                    frame = 3
                    ltr_unlm_cmd = 17
                    cond_yaw_cmd = 115
                    param1 = 0.0
                    param2 = 0.0
                    param3 = 0.0
                    param4 = 0.0
                    x = tup[0]
                    y = tup[1]
                    z = self.H

                    # writing the conditional yaw
                    f.write(
                        "{}\t0\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t1\n".format(
                            seq,
                            frame,
                            cond_yaw_cmd,
                            self.line_bearing,
                            param2,
                            param3,
                            param4,
                            0,
                            0,
                            0,
                        )
                    )

                    # writing the coordinate
                    f.write(
                        "{}\t0\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t1\n".format(
                            seq + 1,
                            frame,
                            ltr_unlm_cmd,
                            param1,
                            param2,
                            param3,
                            param4,
                            x,
                            y,
                            z,
                        )
                    )

    def clicked_test_upload_waypoints(self):
        pass

    def calculate_waypoints_frontback(self, direction):
        """
        Generate Waypoints for CMR for single survey line.

        towards and away from a single common point.

        Parameters
        ----------
        direction : int
            values: (-1 or 1)
            waypoints on the cw direction of the line = 1
            waypoints on the ccw direction of the line = -1.

        Returns
        -------
        waypoints : list
            set of waypoints for either side of the line.

        """
        waypoints = []

        # Bearing of the Grid line
        self.line_bearing = self.get_bearing(
            self.start_lat, self.start_lon, self.end_lat, self.end_lon
        )
        line_length = self.get_distance(
            self.start_lat, self.start_lon, self.end_lat, self.end_lon
        )
        m = self.H * math.tan(math.radians(self.theta_max))
        n = self.H * math.tan(math.radians(self.theta_min))
        k = m - n

        # First waypoint
        wp1 = self.get_new_coordinates(
            self.start_lat,
            self.start_lon,
            m,
            self.line_bearing + direction * 90,
        )
        waypoints.append(wp1)

        # 2nd survey towards the survey line
        wp = self.get_new_coordinates(
            self.start_lat,
            self.start_lon,
            n,
            self.line_bearing + direction * 90,
        )
        waypoints.append(wp)

        total_s = 25
        new_stopping_wp = wp1

        while total_s < line_length:

            # away from the survey line
            waypoints.append(new_stopping_wp)

            # towards a new point
            wp_new = self.get_new_coordinates(
                new_stopping_wp[0],
                new_stopping_wp[1],
                self.s,
                self.line_bearing,
            )
            waypoints.append(wp_new)

            # towards the survey line
            wp = self.get_new_coordinates(
                wp_new[0], wp_new[1], k, self.line_bearing - direction * 90
            )
            waypoints.append(wp)

            new_stopping_wp = wp_new
            total_s += self.s

        return waypoints

    def calculate_waypoints_S(self, direction):
        """
        Generate Waypoints for CMR for single survey line.

        S-shaped plan.

        Parameters
        ----------
        direction : int
            values: (-1 or 1)
            waypoints on the cw direction of the line = 1
            waypoints on the ccw direction of the line = -1.

        Returns
        -------
        waypoints : list
            set of waypoints for either side of the line.

        """
        waypoints = []

        # Bearing of the Grid line
        self.line_bearing = self.get_bearing(
            self.start_lat, self.start_lon, self.end_lat, self.end_lon
        )
        line_length = self.get_distance(
            self.start_lat, self.start_lon, self.end_lat, self.end_lon
        )
        m = self.H * math.tan(math.radians(self.theta_max))
        n = self.H * math.tan(math.radians(self.theta_min))
        k = m - n

        # First waypoint
        wp1 = self.get_new_coordinates(
            self.start_lat,
            self.start_lon,
            m,
            self.line_bearing + direction * 90,
        )
        waypoints.append(wp1)

        # 2nd survey towards the survey line
        wp = self.get_new_coordinates(
            self.start_lat,
            self.start_lon,
            n,
            self.line_bearing + direction * 90,
        )
        waypoints.append(wp)

        # Away from the survey line
        waypoints.append(wp1)

        total_s = 50
        new_stopping_wp = wp1

        while total_s < line_length:

            # to a new point
            wp = self.get_new_coordinates(
                new_stopping_wp[0],
                new_stopping_wp[1],
                self.s,
                self.line_bearing,
            )
            waypoints.append(wp)

            # towards the survey line
            wp = self.get_new_coordinates(
                wp[0], wp[1], k, self.line_bearing - direction * 90
            )
            waypoints.append(wp)

            # to a new point
            wp = self.get_new_coordinates(
                wp[0], wp[1], self.s, self.line_bearing
            )
            waypoints.append(wp)

            # away from the survey line
            wp = self.get_new_coordinates(
                wp[0], wp[1], k, self.line_bearing + direction * 90
            )
            waypoints.append(wp)

            new_stopping_wp = wp
            total_s += self.s * 2

        return waypoints

    def get_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculates the distances between two points.

        Parameters
        ----------
        lat1 : float
            latitude of first point.
        lon1 : float
            longitude of first point.
        lat2 : float
            latitude of end point.
        lon2 : float
            longitude of end point.

        Returns
        -------
        d: float
            Distance between two points (in meters)
        """
        R = 6378100
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        del_lat = lat2 - lat1
        del_lon = lon2 - lon1
        a = (math.sin(del_lat / 2)) ** 2 + math.cos(lat1) * math.cos(
            lat2
        ) * (math.sin(del_lon / 2)) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return d

    def get_bearing(self, lat1, lon1, lat2, lon2):
        """
        Calculates the bearing of a line with start and end points.

        Parameters
        ----------
        lat1 : float
            latitude of first point.
        lon1 : float
            longitude of first point.
        lat2 : float
            latitude of end point.
        lon2 : float
            longitude of end point.

        Returns
        -------
        bearing : float
            Bearing of the line in degrees.

        """
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        y = math.sin(lon2 - lon1) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(
            lat2
        ) * math.cos(lon2 - lon1)
        theta = math.atan2(y, x)
        bearing = (theta * r2d + 360) % 360
        return bearing

    def get_new_coordinates(self, lat1, lon1, dis, angle):
        """
        Calculates new coordinate from start coordinate, distance, and bearing.

        Parameters
        ----------
        lat1 : float
            latitude of first point.
        lon1 : float
            longitude of first point.
        dis : float
            distance to the new point (in metres).
        angle : float
            bearing to the new point (in degrees).

        Returns
        -------
        lat2 : float
            latitude of new point.
        lon2 : float
            longitude of new point.

        """
        R = 6378100
        angle = (angle + 360) % 360
        angle = math.radians(angle)
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.asin(
            math.sin(lat1) * math.cos(dis / R)
            + math.cos(lat1) * math.sin(dis / R) * math.cos(angle)
        )
        lon2 = lon1 + math.atan2(
            math.sin(angle) * math.sin(dis / R) * math.cos(lat1),
            math.cos(dis / R) - math.sin(lat1) * math.sin(lat2),
        )
        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)
        return (lat2, lon2)

    def clicked_draw_grid(self):
        """
        FOR NOW, JUST DOING ONE LINE.

        Calculates the coordinates of the grid lines.

        Returns
        -------
        None.

        """
        grid_points = []
        self.start_lat = float(self.lineEdit_start_lat.text())
        self.start_lon = float(self.lineEdit_start_lon.text())
        self.end_lat = float(self.lineEdit_end_lat.text())
        self.end_lon = float(self.lineEdit_end_lon.text())

        grid_points.append((self.start_lat, self.start_lon))
        grid_points.append((self.end_lat, self.end_lon))

        self.widget_cmr_map.add_grid_lines(grid_points)
        self.checkBox_grid.setChecked(True)

    def grid_checkbox_changed(self):
        if self.checkBox_grid.isChecked():
            self.widget_cmr_map.change_grid_line_state(1)
        else:
            self.widget_cmr_map.change_grid_line_state(0)

    def waypoints_checkbox_changed(self):
        if self.checkBox_waypoints.isChecked():
            self.widget_cmr_map.change_waypoints_line_state(1)
        else:
            self.widget_cmr_map.change_waypoints_line_state(0)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)

        pixmap = QtGui.QPixmap(
            self.ctx.get_resource("cmr_planning/cmr_schematic.jpeg")
        )
        self.label_schematic.setPixmap(pixmap)

        self.widget_cmr_map.setup_qml(self.ctx)

        self.checkBox_waypoints.setTristate(False)
        self.checkBox_grid.setTristate(False)
        self.set_default_values()

    def set_default_values(self):
        self.lineEdit_start_lat.setText(str(33.19389))
        self.lineEdit_start_lon.setText(str(-87.48133))
        self.lineEdit_end_lat.setText(str(33.19165))
        self.lineEdit_end_lon.setText(str(-87.48089))
        self.lineEdit_rel_height.setText(str(30))
        self.lineEdit_spacing.setText(str(45))
        self.lineEdit_theta_max.setText(str(60))
        self.lineEdit_theta_min.setText(str(15))

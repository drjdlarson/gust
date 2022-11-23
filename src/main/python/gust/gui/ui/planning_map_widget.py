#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 16:58:22 2022

@author: lagerprocessor
"""
import os
import time
import random
import math
import pathlib
import matplotlib.image as mpimg
from PyQt5 import QtCore, QtWidgets, QtQuickWidgets, QtPositioning, QtQuickWidgets
from PyQt5.QtCore import QTimer, QTemporaryDir, QFile, QAbstractListModel, Qt, QByteArray, QModelIndex, QVariant


# TODO: Replace the Test Class and fix file paths to use ctx

class PlanningMapWidget(QtQuickWidgets.QQuickWidget):

    def __init__(self, parent=None):
        super(PlanningMapWidget, self).__init__(parent,
                                                resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        self._grid = None
        self._waypoints = None

# %%
    # FOR TESTING ONLY
    def setup_qml_for_test(self, resource_path):
        qml_file = 'ui/planning_map.qml'

        self.temp_dir = QTemporaryDir()

        if self.temp_dir.isValid():
            temp_path = self.temp_dir.path()
            temp_map_file = QFile(temp_path + "/temp_planning_map.qml")
            with open(qml_file, 'rt') as fin:
                with open(temp_path + "/temp_planning_map.qml", 'wt') as fout:
                    replacing_str = [("MAP_FilledByMapWidget", resource_path + "/offline_folders/"),
                                     ("CACHE_FilledByMapWidget", temp_path + "/")]
                    lines = fin.readlines()
                    text = ''.join(lines)
                    for old, new in replacing_str:
                        text = text.replace(old, new)
                    fout.write(text)

            # QFile.copy(temp_path + "/temp_map.qml", resource_path + "/from_temp_qml")

        self.engine().clearComponentCache()
        self.setSource(QtCore.QUrl.fromLocalFile(temp_path + "/temp_planning_map.qml"))

        self._grid = GridLines(self)
        self.rootContext().setContextProperty("grid_line", self._grid)

        self._waypoints = WaypointLines()
        self.rootContext().setContextProperty("waypoint_line", self._waypoints)
# %%

    def setup_qml(self, ctx):
        self.ctx = ctx
        qml_file = self.ctx.get_resource("map_widget/map.qml")
        resource_file = self.ctx.get_resource('map_widget/README')
        resource_path = str(pathlib.Path(resource_file).parent.resolve())

        self.temp_dir = QTemporaryDir();

        if self.temp_dir.isValid():
            temp_path = self.temp_dir.path()
            temp_map_file = QFile(temp_path + "/temp_map.qml")
            with open(qml_file, 'rt') as fin:
                with open(temp_path + "/temp_map.qml", 'wt') as fout:
                    replacing_str = [("MAP_FilledByMapWidget", resource_path + "/offline_folders/"),
                                     ("CACHE_FilledByMapWidget", temp_path + "/")]
                    lines = fin.readlines()
                    text = ''.join(lines)
                    for old, new in replacing_str:
                        text = text.replace(old, new)
                    fout.write(text)

            # QFile.copy(temp_path + "/temp_map.qml", resource_path + "/from_temp_qml")

        self.engine().clearComponentCache()
        self.setSource(QtCore.QUrl.fromLocalFile(temp_path + "/temp_map.qml"))


    def display_grid_lines(self, coordinates):
        if self._grid is not None:
            q_coordinates = [QtPositioning.QGeoCoordinate(*ii) for ii in coordinates]
            self._grid.add_grid_lines(q_coordinates)

    def display_waypoint_lines(self, coordinates, color):
        if self._waypoints is not None:
            q_coordinates = [QtPositioning.QGeoCoordinate(*ii) for ii in coordinates]
            self._waypoints.add_waypoint_lines(
                {"wp_coordinates": q_coordinates,
                 "color": color}
                )

    def clear_grid_lines(self):
        if self._grid is not None:
            self._grid.remove_grid_lines()
            self._grid.add_grid_lines()

class GridLines(QAbstractListModel):
    PositionRole = Qt.UserRole + 1

    def __init__(self, parent=None):
        super(GridLines, self).__init__(parent)
        self._grid_lines = []

    def rowCount(self, index=QModelIndex()):
        return len(self._grid_lines)

    def roleNames(self):
        return {
            GridLines.PositionRole: b"grid_coordinates"
            }

    def data(self, index, role=Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == GridLines.PositionRole:
                return self._grid_lines[index.row()]
        return QVariant()

    def add_grid_lines(self, coordinates=None):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._grid_lines.append(coordinates)
        self.endInsertRows()

    def remove_grid_lines(self):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._grid_lines = []
        self.endInsertRows()

        print("it should be removed now")

class WaypointLines(QAbstractListModel):
    PositionRole = Qt.UserRole + 1
    ColorRole = Qt.UserRole + 2

    def __init__(self, parent=None):
        super(WaypointLines, self).__init__(parent)
        self._waypoint_lines = []

    def rowCount(self, index=QModelIndex()):
        return len(self._waypoint_lines)

    def roleNames(self):
        return {
            WaypointLines.PositionRole: b"wp_coordinates",
            WaypointLines.ColorRole: b"wp_color"
            }

    def data(self, index, role=Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == WaypointLines.PositionRole:
                return self._waypoint_lines[index.row()]['wp_coordinates']
            elif role == WaypointLines.ColorRole:
                return self._waypoint_lines[index.row()]['color']
        return QVariant()

    def add_waypoint_lines(self, waypoints):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._waypoint_lines.append(waypoints)
        self.endInsertRows()

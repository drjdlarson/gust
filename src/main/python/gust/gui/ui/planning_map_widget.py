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
from functools import partial
from PyQt5 import QtCore, QtWidgets, QtQuickWidgets, QtPositioning, QtQuickWidgets
from PyQt5.QtCore import QTimer, QTemporaryDir, QFile, QAbstractListModel, Qt, QByteArray, QModelIndex, QVariant


# TODO: Replace the Test Class and fix file paths to use ctx

class PlanningMapWidget(QtQuickWidgets.QQuickWidget):

    def __init__(self, parent=None):
        super(PlanningMapWidget, self).__init__(parent,
                                                resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        self._grid_line = None
        self._waypoints_line = None


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
        if self._grid_line is None:
            self._grid_line = Lines()
            self.rootContext().setContextProperty("line_item", self._grid_line)

            self._grid_line.color = "yellow"
            q_coordinates = [QtPositioning.QGeoCoordinate(*ii) for ii in coordinates]
            self._grid_line.path = q_coordinates

    def display_waypoint_lines(self, coordinates, color):
        if self._waypoints_line is None:
            self._waypoints_line = Lines()
            self.rootContext().setContextProperty("line_item", self._waypoints_line)

            self._waypoints_line.color = color
            q_coordinates = [QtPositioning.QGeoCoordinate(*ii) for ii in coordinates]
            self._waypoints_line.path = q_coordinates

    def change_grid_line_color(self, color):
        if self._grid_line is not None:
            self._grid_line.color = color


class Lines(QAbstractListModel):
    pathChanged = QtCore.pyqtSignal(list)
    colorChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(Lines, self).__init__(parent)
        self._color = "black"
        self._path = None

    @QtCore.pyqtProperty(str, notify=colorChanged)
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        if self._color != new_color:
            self._color = new_color
            self.colorChanged.emit(new_color)

    @QtCore.pyqtProperty(list, notify=pathChanged)
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        if self._path != new_path:
            self._path = new_path
            self.pathChanged.emit(new_path)

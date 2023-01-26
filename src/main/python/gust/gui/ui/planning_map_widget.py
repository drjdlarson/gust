"""Map Widget for all planning windows"""
import os
import time
import random
import math
import pathlib
import matplotlib.image as mpimg
from functools import partial
from PyQt5 import QtCore, QtWidgets, QtQuickWidgets, QtPositioning, QtQuickWidgets
from PyQt5.QtCore import QTimer, QTemporaryDir, QFile, QAbstractListModel, Qt, QByteArray, QModelIndex, QVariant


class PlanningMapWidget(QtQuickWidgets.QQuickWidget):

    def __init__(self, parent=None):
        super(PlanningMapWidget, self).__init__(parent,
                                                resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        self._grid_line_names = []
        self._waypoint_line_names = []

    def setup_qml(self, ctx):
        self.ctx = ctx
        qml_file = self.ctx.get_resource("cmr_planning/planning_map.qml")
        resource_file = self.ctx.get_resource('cmr_planning/README')
        resource_path = str(pathlib.Path(resource_file).parent.resolve())

        self.temp_dir = QTemporaryDir();

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

        self.line_model = LineModel()
        self.rootContext().setContextProperty("line_model", self.line_model)

    def change_grid_line_state(self, val):
        if self._grid_line_names:
            if val == 1:
                self.line_model.change_line_color("yellow_grid", "yellow")
            else:
                self.line_model.change_line_color("yellow_grid", "transparent")

    def change_waypoints_line_state(self, val):
        if self._waypoint_line_names:
            for name in self._waypoint_line_names:
                color = name.split("_")[0]
                if val == 1:
                    self.line_model.change_line_color(name, color)
                else:
                    self.line_model.change_line_color(name, "transparent")

    def add_grid_lines(self, coordinates):
        grid_line = Lines()
        grid_line.setColor("yellow")
        qcoordinates = [QtPositioning.QGeoCoordinate(*ii) for ii in coordinates]
        grid_line.setPath(qcoordinates)
        self.line_model.addLine("yellow_grid", grid_line)

        self._grid_line_names.append("yellow_grid")

    def add_waypoint_lines(self, coordinates, color):
        wp_line = Lines()
        wp_line.setColor(color)
        qcoordinates = [QtPositioning.QGeoCoordinate(*ii) for ii in coordinates]
        wp_line.setPath(qcoordinates)
        self.line_model.addLine("{}_wp".format(color), wp_line)

        self._waypoint_line_names.append("{}_wp".format(color))

class Lines(QAbstractListModel):
    pathChanged = QtCore.pyqtSignal(list)
    colorChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(Lines, self).__init__(parent)
        self._color = "black"
        self._path = None

    def color_val(self):
        return self._color

    def setColor(self, new_color):
        self._color = new_color
        self.colorChanged.emit(new_color)

    def path_val(self):
        return self._path

    def setPath(self, new_path):
        self._path = new_path
        self.pathChanged.emit(new_path)


class LineModel(QAbstractListModel):
    PathRole = Qt.UserRole + 1
    ColorRole = Qt.UserRole + 2

    _roles = {PathRole: QByteArray(b"line_path"), ColorRole: QByteArray(b"line_color")}

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._lines = []
        self.object_names = []

    def rowCount(self, index=QModelIndex()):
        return len(self._lines)

    def roleNames(self):
        return self._roles

    def data(self, index, role=Qt.DisplayRole):
        if index.row() >= self.rowCount():
            return QVariant()
        line = self._lines[index.row()]

        if role == LineModel.PathRole:
            return line.path_val()
        elif role == LineModel.ColorRole:
            return line.color_val()

        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            line = self._lines[index.row()]
            if role == LineModel.PathRole:
                line.setPath(value)
            elif role == LineModel.ColorRole:
                line.setColor(value)
            self.dataChanged.emit(index, index)
            return True
        return QAbstractListModel.setData(self, index, value, role)

    def addLine(self, name, line):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._lines.append(line)
        self.endInsertRows()
        self.object_names.append(name)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractListModel.flags(index)|Qt.ItemIsEditable

    def change_line_color(self, name, new_color):
        if name in self.object_names:
            ind = self.index(self.object_names.index(name), 0)
            self.setData(ind, new_color, LineModel.ColorRole)
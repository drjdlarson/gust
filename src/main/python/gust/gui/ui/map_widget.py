import os
import time
import random
import math
import pathlib
import matplotlib.image as mpimg
from PyQt5 import QtCore, QtWidgets, QtQuickWidgets, QtPositioning, QtQuickWidgets
from PyQt5.QtCore import QTimer, QTemporaryDir, QFile


class MapWidget(QtQuickWidgets.QQuickWidget):

    def __init__(self, parent=None):
        self.vehicle_list = {}
        self.temp_dir = None
        super(MapWidget, self).__init__(parent,
                                            resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView)

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

    def clear_drone_list(self):
        self.vehicle_list = {}

    def remove_vehicle_from_map(self, name):
        # self.rootContext().setContextProperty("markermodel", None)
        # self.rootContext().setContextProperty("yaw_line", None)
        # self.rootContext().setContextProperty("heading_line", None)
        # self.rootContext().setContextProperty("homemodel", None)
        self.vehicle_list[name].clear_items()
        self.vehicle_list.pop(name)
        # self.update()

    def add_drone(self, name, color, home_lat, home_lon, latitude, longitude, yaw, heading, mode):

        # fix this later
        self.clear_drone_list()

        if name not in self.vehicle_list:
            marker = MarkerModel(self)
            self.rootContext().setContextProperty("markermodel", marker)

            yaw_line = yawLineModel(self)
            self.rootContext().setContextProperty("yaw_line", yaw_line)

            heading_line = headingLineModel(self)
            self.rootContext().setContextProperty("heading_line", heading_line)

            home = HomeMarkerModel(self)
            self.rootContext().setContextProperty("homemodel", home)

            self.vehicle_list[name] = MapHelper(name, color, marker, yaw_line, heading_line, home, home_lat, home_lon, latitude, longitude, yaw, heading, mode, self.ctx,)
        else:
            self.vehicle_list[name].home_lat = home_lat
            self.vehicle_list[name].home_lon = home_lon
            self.vehicle_list[name].latitude = latitude
            self.vehicle_list[name].longitude = longitude
            self.vehicle_list[name].yaw = yaw
            self.vehicle_list[name].heading = heading
            self.vehicle_list[name].mode = mode

    def update_map(self):
        for vehicle in self.vehicle_list.values():
            vehicle.update_map()


class MapHelper():
    def __init__(self, name, color, marker, yaw_line, heading_line, home, home_lat, home_lon, latitude, longitude, yaw, heading, mode, ctx):
        self.name = name
        self.color = color
        self.marker = marker
        self.yaw_line = yaw_line
        self.heading_line = heading_line
        self.home = home
        self.home_lat = home_lat
        self.home_lon = home_lon
        self.latitude = latitude
        self.longitude = longitude
        self.yaw = yaw
        self.heading = heading
        self.mode = mode
        self.ctx = ctx

    def update_map(self):
        self.icon = self.icon_selector()
        pos = (self.latitude, self.longitude)
        pos_coord = QtPositioning.QGeoCoordinate(*pos)
        self.marker.appendMarker(
            {"position": pos_coord,
             "source": self.icon_selector(),
             "yaw": self.yaw,
             }
        )

        yaw_coord = QtPositioning.QGeoCoordinate(*self.get_points(self.yaw))
        yaw_path = [pos_coord, yaw_coord]
        self.yaw_line.appendLine({"yaw_path": yaw_path})

        heading_coord = QtPositioning.QGeoCoordinate(*self.get_points(self.heading))
        heading_path = [pos_coord, heading_coord]
        self.heading_line.appendLine({"heading_path": heading_path})

        file = 'map_widget/colored_icons/' + self.color + '_home.png'
        home_icon = self.ctx.get_resource(file)
        home = (self.home_lat, self.home_lon)
        home_coord = QtPositioning.QGeoCoordinate(*home)
        self.home.appendMarker(
            {"home": home_coord,
              "source": home_icon,
              "name": self.name,
                }
            )

    def get_points(self, angle):
        R = 6378.1
        dis = 1
        angle = math.radians(angle)
        lat_1 = math.radians(self.latitude)
        lon_1 = math.radians(self.longitude)
        lat_2 = math.asin(math.sin(lat_1) * math.cos(dis / R) + math.cos(lat_1) * math.sin(dis / R) * math.cos(angle))
        lon_2 = lon_1 + math.atan2(math.sin(angle) * math.sin(dis / R) * math.cos(lat_1),
                                   math.cos(dis / R) - math.sin(lat_1) * math.sin(lat_2))
        lat_2 = math.degrees(lat_2)
        lon_2 = math.degrees(lon_2)
        return (lat_2, lon_2)

    def icon_selector(self):
        if self.mode == "stabilize".upper():
            file = 'map_widget/colored_icons/' + self.color + '_pos.png'
            icon_type = self.ctx.get_resource(file)
        elif self == "auto".upper():
            file = 'map_widget/colored_icons/' + self.color + '_rtl_pos.png'
            icon_type = self.ctx.get_resource(file)
        else:
            file = 'map_widget/colored_icons/' + self.color + '_spos.png'
            icon_type = self.ctx.get_resource(file)
        return icon_type

    def clear_items(self):
        self.marker.remove_marker()
        self.yaw_line.remove_lines()
        self.heading_line.remove_lines()
        self.home.remove_marker()


class MarkerModel(QtCore.QAbstractListModel):
    PositionRole, SourceRole, yawRole = range(QtCore.Qt.UserRole, QtCore.Qt.UserRole + 3)

    def __init__(self, parent=None):
        super(MarkerModel, self).__init__(parent)
        self._markers = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._markers)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == MarkerModel.PositionRole:
                return self._markers[index.row()]["position"]
            elif role == MarkerModel.SourceRole:
                return self._markers[index.row()]["source"]
            elif role == MarkerModel.yawRole:
                return self._markers[index.row()]["yaw"]
        return QtCore.QVariant()

    def roleNames(self):
        return {
            MarkerModel.PositionRole: b"position_marker",
            MarkerModel.SourceRole: b"source_marker",
            MarkerModel.yawRole: b"rotation_marker"}

    def remove_marker(self):
        if self.rowCount() == 0:
            return
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount())
        for ii in range(len(self._markers)-1, -1, -1):
            del self._markers[ii]
        # self._markers = []
        self.endRemoveRows()

    def update_marker(self, marker):
        if not self._markers:
            self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
            self._markers.append(marker)
            self.endInsertRows()
        else:
            print("In the else part")
            self._markers[0]['position'].setLatitude(marker['position'].latitude())
            print(self._markers[0]['position'].latitude())

            # self._markers[0]['source'] = marker['source']
            # self._markers[0]['yaw'] = marker['yaw']
            # del self._markers[0]
            # self._markers.append(marker)
            # self._markers[0] = marker

    def appendMarker(self, marker):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._markers.append(marker)
        self.endInsertRows()


class HomeMarkerModel(QtCore.QAbstractListModel):
    HomeRole, SourceRole, NameRole = range(QtCore.Qt.UserRole, QtCore.Qt.UserRole + 3)

    def __init__(self, parent=None):
        super(HomeMarkerModel, self).__init__(parent)
        self._homes = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._homes)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == HomeMarkerModel.HomeRole:
                return self._homes[index.row()]['home']
            elif role == HomeMarkerModel.SourceRole:
                return self._homes[index.row()]['source']
            elif role == HomeMarkerModel.NameRole:
                return self._homes[index.row()]['name']
        return QtCore.QVariant()

    def roleNames(self):
        return {
            HomeMarkerModel.HomeRole: b"home_marker",
            HomeMarkerModel.SourceRole: b"home_source",
            HomeMarkerModel.NameRole: b"name"
            }

    def remove_marker(self):
        if self.rowCount() == 0:
            return
        self.beginRemoveRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._homes = []
        self.endRemoveRows()

    def update_marker(self, marker):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        if not self._homes:
            self._homes.append(marker)
        else:
            self._homes[-1].update(marker)
        self.endInsertRows()

    def appendMarker(self, marker):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._homes.append(marker)
        self.endInsertRows()

class yawLineModel(QtCore.QAbstractListModel):
    yawPath = QtCore.Qt.UserRole

    def __init__(self, parent=None):
        super(yawLineModel, self).__init__(parent)
        self._yawlines = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._yawlines)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == yawLineModel.yawPath:
                return self._yawlines[index.row()]["yaw_path"]
        return QtCore.QVariant()

    def roleNames(self):
        return {
            yawLineModel.yawPath: b"yaw_path",
        }

    def remove_lines(self):
        if self.rowCount() == 0:
            return
        self.beginRemoveRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._yawlines = []
        self.endRemoveRows()

    def update_line(self, line):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        if not self._yawlines:
            self._yawlines.append(line)
        else:
            self._yawlines[-1].update(line)
        self.endInsertRows()

    def appendLine(self, line):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._yawlines.append(line)
        self.endInsertRows()

class headingLineModel(QtCore.QAbstractListModel):
    headingPath = QtCore.Qt.UserRole

    def __init__(self, parent=None):
        super(headingLineModel, self).__init__(parent)
        self._headinglines = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._headinglines)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == headingLineModel.headingPath:
                return self._headinglines[index.row()]["heading_path"]
        return QtCore.QVariant()

    def roleNames(self):
        return {
            headingLineModel.headingPath: b"heading_path",
        }

    def remove_lines(self):
        if self.rowCount() == 0:
            return
        self.beginRemoveRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._headinglines = []
        self.endRemoveRows()

    def update_line(self, line):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        if not self._headinglines:
            self._headinglines.append(line)
        else:
            self._headinglines[-1].update(line)
        self.endInsertRows()

    def appendLine(self, line):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._headinglines.append(line)
        self.endInsertRows()




if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MapWidget()

    w.show()
    sys.exit(app.exec_())

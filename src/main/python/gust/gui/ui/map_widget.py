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
        super(MapWidget, self).__init__(parent,
                                            resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView)

    def setup_qml(self, ctx):
        self.ctx = ctx
        qml_file = os.path.join(os.path.dirname(__file__), "map.qml")
        resource_file = self.ctx.get_resource('map_widget/README')
        resource_path = str(pathlib.Path(resource_file).parent.resolve())

        temp_dir = QTemporaryDir();

        if temp_dir.isValid():
            temp_path = temp_dir.path()
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

            QFile.copy(temp_path + "/temp_map.qml", resource_path + "/from_temp_qml")

        self.engine().clearComponentCache()
        self.setSource(QtCore.QUrl.fromLocalFile(temp_path + "/temp_map.qml"))
        self.rootObject().setProperty("customHost", "file:offline_test/")

    def remove_vehicle_from_map(self, name):
        self.vehicle_list.pop(name)

    def clear_drone_list(self):
        self.vehicle_list = {}

    def add_drone(self, name, home_lat, home_lon, latitude, longitude, heading, track, mode):
        if name not in self.vehicle_list:
            marker = MarkerModel(self)
            self.rootContext().setContextProperty("markermodel", marker)

            hdg_line = HeadingLineModel(self)
            self.rootContext().setContextProperty("heading_line", hdg_line)

            track_line = TrackLineModel(self)
            self.rootContext().setContextProperty("track_line", track_line)

            home = HomeMarkerModel(self)
            self.rootContext().setContextProperty("homemodel", home)

            self.vehicle_list[name] = MapHelper(name, marker, hdg_line, track_line, home, home_lat, home_lon, latitude, longitude, heading, track, mode, self.ctx,)
        else:
            self.vehicle_list[name].home_lat = home_lat
            self.vehicle_list[name].home_lon = home_lon
            self.vehicle_list[name].latitude = latitude
            self.vehicle_list[name].longitude = longitude
            self.vehicle_list[name].heading = heading
            self.vehicle_list[name].track = track
            self.vehicle_list[name].mode = mode

    def update_map(self):
        for vehicle in self.vehicle_list.values():
            vehicle.update_map()


class MapHelper():
    def __init__(self, name, marker, hdg_line, track_line, home, home_lat, home_lon, latitude, longitude, heading, track, mode, ctx):
        self.name = name
        self.marker = marker
        self.hdg_line = hdg_line
        self.track_line = track_line
        self.home = home
        self.home_lat = home_lat
        self.home_lon = home_lon
        self.latitude = latitude
        self.longitude = longitude
        self.heading = heading
        self.track = track
        self.mode = mode
        self.ctx = ctx

    def update_map(self):
        self.icon = self.icon_selector()
        pos = (self.latitude, self.longitude)
        pos_coord = QtPositioning.QGeoCoordinate(*pos)
        self.marker.appendMarker(
            {"position": pos_coord,
             "source": self.icon_selector(),
             "heading": self.heading,
             }
        )

        hdg_coord = QtPositioning.QGeoCoordinate(*self.get_points(self.heading))
        hdg_path = [pos_coord, hdg_coord]
        self.hdg_line.appendLine({"heading_path": hdg_path})

        track_coord = QtPositioning.QGeoCoordinate(*self.get_points(self.track))
        track_path = [pos_coord, track_coord]
        self.track_line.appendLine({"track_path": track_path})

        file = 'map_widget/' + self.name + '_home.png'
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
            file = 'map_widget/' + self.name + '_pos.png'
            icon_type = self.ctx.get_resource(file)
        elif self == "auto".upper():
            file = 'map_widget/' + self.name + '_rtl_pos.png'
            icon_type = self.ctx.get_resource(file)
        else:
            file = 'map_widget/' + self.name + '_spos.png'
            icon_type = self.ctx.get_resource(file)
        return icon_type


class MarkerModel(QtCore.QAbstractListModel):
    PositionRole, SourceRole, HeadingRole = range(QtCore.Qt.UserRole, QtCore.Qt.UserRole + 3)

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
            elif role == MarkerModel.HeadingRole:
                return self._markers[index.row()]["heading"]
        return QtCore.QVariant()

    def roleNames(self):
        return {
            MarkerModel.PositionRole: b"position_marker",
            MarkerModel.SourceRole: b"source_marker",
            MarkerModel.HeadingRole: b"rotation_marker"}

    def remove_marker(self):
        if self.rowCount() == 0:
            return
        self.beginRemoveRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._markers = []
        self.endRemoveRows()

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

    def appendMarker(self, marker):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._homes.append(marker)
        self.endInsertRows()

class HeadingLineModel(QtCore.QAbstractListModel):
    HeadingPath = QtCore.Qt.UserRole

    def __init__(self, parent=None):
        super(HeadingLineModel, self).__init__(parent)
        self._hdglines = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._hdglines)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == HeadingLineModel.HeadingPath:
                return self._hdglines[index.row()]["heading_path"]
        return QtCore.QVariant()

    def roleNames(self):
        return {
            HeadingLineModel.HeadingPath: b"heading_path",
        }

    def remove_lines(self):
        if self.rowCount() == 0:
            return
        self.beginRemoveRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._hdglines = []
        self.endRemoveRows()

    def appendLine(self, line):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._hdglines.append(line)
        self.endInsertRows()

class TrackLineModel(QtCore.QAbstractListModel):
    TrackPath = QtCore.Qt.UserRole

    def __init__(self, parent=None):
        super(TrackLineModel, self).__init__(parent)
        self._tracklines = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._tracklines)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == TrackLineModel.TrackPath:
                return self._tracklines[index.row()]["track_path"]
        return QtCore.QVariant()

    def roleNames(self):
        return {
            TrackLineModel.TrackPath: b"track_path",
        }

    def remove_lines(self):
        if self.rowCount() == 0:
            return
        self.beginRemoveRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._tracklines = []
        self.endRemoveRows()

    def appendLine(self, line):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._tracklines.append(line)
        self.endInsertRows()




if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MapWidget()

    w.show()
    sys.exit(app.exec_())

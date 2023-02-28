"""Map Widget for the main frontend window"""
import os
import time
import random
import math
import pathlib
from PyQt5 import (
    QtCore,
    QtPositioning,
    QtQuickWidgets,
)
from PyQt5.QtCore import (
    QTimer,
    QTemporaryDir,
    QFile,
    QAbstractListModel,
    Qt,
    QByteArray,
    QModelIndex,
    QVariant,
)


class MapWidget(QtQuickWidgets.QQuickWidget):
    def __init__(self, parent=None):
        super(MapWidget, self).__init__(
            parent,
            resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView,
        )
        self._vehicles = {}
        self._vehicles_mission = {}
        self._vehicle_color = {}

    def setup_qml(self, ctx):
        self.ctx = ctx
        qml_file = self.ctx.get_resource("map_widget/map.qml")
        resource_file = self.ctx.get_resource("map_widget/README")
        resource_path = str(pathlib.Path(resource_file).parent.resolve())

        self.temp_dir = QTemporaryDir()

        if self.temp_dir.isValid():
            temp_path = self.temp_dir.path()
            temp_map_file = QFile(temp_path + "/temp_map.qml")
            with open(qml_file, "rt") as fin:
                with open(temp_path + "/temp_map.qml", "wt") as fout:
                    replacing_str = [
                        (
                            "MAP_FilledByMapWidget",
                            resource_path + "/offline_folders/",
                        ),
                        ("CACHE_FilledByMapWidget", temp_path + "/"),
                    ]
                    lines = fin.readlines()
                    text = "".join(lines)
                    for old, new in replacing_str:
                        text = text.replace(old, new)
                    fout.write(text)

            # QFile.copy(temp_path + "/temp_map.qml", resource_path + "/from_temp_qml")

        self.engine().clearComponentCache()
        self.setSource(QtCore.QUrl.fromLocalFile(temp_path + "/temp_map.qml"))

        self.marker_model = MarkerModel(self)
        self.rootContext().setContextProperty("markermodel", self.marker_model)

        self.heading_line_model = HeadingLineModel(self)
        self.rootContext().setContextProperty(
            "heading_line", self.heading_line_model
        )

        self.yaw_line_model = YawLineModel(self)
        self.rootContext().setContextProperty("yaw_line", self.yaw_line_model)

        self.home_model = HomeModel()
        self.rootContext().setContextProperty("homemodel", self.home_model)

        self.flight_path_model = FlightLineModel(self)
        self.rootContext().setContextProperty("flight_line", self.flight_path_model)

        self.waypoint_model = WaypointModel()
        self.rootContext().setContextProperty("waypointmodel", self.waypoint_model)


    def add_drone(
        self,
        name,
        color,
        home_lat,
        home_lon,
        latitude,
        longitude,
        yaw,
        heading,
        mode,
    ):

        if name not in self._vehicles:
            self._vehicles[name] = MapHelper(
                name,
                color,
                self.marker_model,
                self.heading_line_model,
                self.yaw_line_model,
                self.home_model,
                home_lat,
                home_lon,
                latitude,
                longitude,
                yaw,
                heading,
                mode,
                self.ctx,
            )
            self._vehicle_color[name] = color
            self._vehicles[name].add_objects_in_map()
        else:
            self._vehicles[name].home_lat = home_lat
            self._vehicles[name].home_lon = home_lon
            self._vehicles[name].latitude = latitude
            self._vehicles[name].longitude = longitude
            self._vehicles[name].yaw = yaw
            self._vehicles[name].heading = heading
            self._vehicles[name].mode = mode
            self._vehicles[name].update_objects_in_map()

    def display_missions(self, all_waypoints):
        for name, waypoints in all_waypoints.items():
            if name not in self._vehicles_mission.keys():
                self._vehicles_mission[name] = FlightPlanHelper(
                    name,
                    self._vehicle_color[name],
                    self.waypoint_model,
                    self.flight_path_model,
                    self.ctx
                )
                self._vehicles_mission[name].display_new_mission(waypoints)
            else:
                self._vehicles_mission[name].display_updated_mission(waypoints)

    def remove_vehicle_from_map(self, name):
        if name in self._vehicles:

            # removing the Position, Yaw, Heading, Home Models
            self._vehicles[name].remove_all_models()
            del self._vehicles[name]

            # removing the Waypoints and Flight Path models
            self._vehicles_mission[name].remove_waypoints_and_lines()
            del self._vehicles_mission[name]


class FlightPlanHelper:
    def __init__(self, name, color, waypoint_model, flight_path_model, ctx):
        self.name = name
        self.color = color
        self.waypoint_model = waypoint_model
        self.flight_path_model = flight_path_model
        self.ctx = ctx

    def remove_waypoints_and_lines(self):
        self.flight_path_model.removePathLine(self.name)
        self.waypoint_model.remove_all_waypoint_markers()

    def display_new_mission(self, waypoints):
        flight_lines, coords = self.prepare_flight_lines_object(waypoints)
        self.flight_path_model.addPathLine(self.name, flight_lines)

        for wp_coord in coords:
            wp_marker = self.prepare_waypoint_marker_object(wp_coord)
            self.waypoint_model.addWaypoint(self.name, wp_marker)

    def display_updated_mission(self, new_waypoints):

        # For flight lines, we can just update the lines
        new_flight_lines, coords = self.prepare_flight_lines_object(new_waypoints)
        self.flight_path_model.updatePathLine(self.name, new_flight_lines)

        # For waypoint markers, we have to remove the waypoint markers and redraw them
        self.waypoint_model.remove_all_waypoint_markers()
        for wp_coord in coords:
            wp_marker = self.prepare_waypoint_marker_object(wp_coord)
            self.waypoint_model.addWaypoint(self.name, wp_marker)

    def prepare_waypoint_marker_object(self, wp_coord):
        wp_marker = Marker()
        file = "map_widget/colored_icons/" + self.color + "_waypoint.png"
        icon_type = self.ctx.get_resource(file)
        wp_marker.setSource(icon_type)
        wp_marker.setPosition(wp_coord)
        return wp_marker
    def prepare_flight_lines_object(self, waypoints):
        flight_lines = Line()
        flight_lines.setColor(self.color)
        qcoordinates = [QtPositioning.QGeoCoordinate(*ii) for ii in waypoints]
        flight_lines.setPath(qcoordinates)
        return flight_lines, qcoordinates

class MapHelper:
    def __init__(
        self,
        name,
        color,
        marker_model,
        heading_model,
        yaw_model,
        home_model,
        home_lat,
        home_lon,
        latitude,
        longitude,
        yaw,
        heading,
        mode,
        ctx,
    ):
        self.name = name
        self.color = color
        self.marker_model = marker_model
        self.heading_model = heading_model
        self.home_model = home_model
        self.yaw_model = yaw_model
        self.home_lat = home_lat
        self.home_lon = home_lon
        self.latitude = latitude
        self.longitude = longitude
        self.yaw = yaw
        self.heading = heading
        self.mode = mode
        self.ctx = ctx

    def remove_all_models(self):
        self.marker_model.removeMarker(self.name)
        self.yaw_model.removeYawLine(self.name)
        self.heading_model.removeHeadingLine(self.name)
        self.home_model.removeHome(self.name)

    def add_objects_in_map(self):
        self.marker_model.addMarker(self.name, self.prepare_marker_object())
        self.yaw_model.addYawLine(
            self.name, self.prepare_line_object("white", self.yaw)
        )
        self.heading_model.addHeadingLine(
            self.name, self.prepare_line_object("black", self.heading)
        )
        self.home_model.addHome(self.name, self.prepare_home_object())

    def update_objects_in_map(self):
        self.marker_model.updateMarker(self.name, self.prepare_marker_object())
        self.yaw_model.updateYawLine(
            self.name, self.prepare_line_object("white", self.yaw)
        )
        self.heading_model.updateHeadingLine(
            self.name, self.prepare_line_object("black", self.heading)
        )
        self.home_model.updateHome(self.name, self.prepare_home_object())

    def prepare_line_object(self, color, angle):
        line = Line()
        line.setColor(color)
        coordinates = [
            (self.latitude, self.longitude),
            self.get_points(angle),
        ]
        qcoordinates = [QtPositioning.QGeoCoordinate(*ii) for ii in coordinates]
        line.setPath(qcoordinates)
        return line

    def prepare_home_object(self):
        home = Marker()
        file = "map_widget/colored_icons/" + self.color + "_home.png"
        home.setSource(self.ctx.get_resource(file))
        home_pos = (self.home_lat, self.home_lon)
        home_pos_coord = QtPositioning.QGeoCoordinate(*home_pos)
        home.setPosition(home_pos_coord)
        return home

    def prepare_marker_object(self):
        marker = Marker()
        marker.setSource(self.drone_icon_selector())
        marker.setRotation(self.yaw)
        pos = (self.latitude, self.longitude)
        pos_coord = QtPositioning.QGeoCoordinate(*pos)
        marker.setPosition(pos_coord)
        return marker

    def get_points(self, angle):
        R = 6378.1
        dis = 1
        angle = math.radians(angle)
        lat_1 = math.radians(self.latitude)
        lon_1 = math.radians(self.longitude)
        lat_2 = math.asin(
            math.sin(lat_1) * math.cos(dis / R)
            + math.cos(lat_1) * math.sin(dis / R) * math.cos(angle)
        )
        lon_2 = lon_1 + math.atan2(
            math.sin(angle) * math.sin(dis / R) * math.cos(lat_1),
            math.cos(dis / R) - math.sin(lat_1) * math.sin(lat_2),
        )
        lat_2 = math.degrees(lat_2)
        lon_2 = math.degrees(lon_2)
        return (lat_2, lon_2)

    def drone_icon_selector(self):
        if self.mode == "stabilize".upper():
            file = "map_widget/colored_icons/" + self.color + "_pos.png"
            icon_type = self.ctx.get_resource(file)
        elif self == "auto".upper():
            file = "map_widget/colored_icons/" + self.color + "_rtl_pos.png"
            icon_type = self.ctx.get_resource(file)
        else:
            file = "map_widget/colored_icons/" + self.color + "_spos.png"
            icon_type = self.ctx.get_resource(file)
        return icon_type


class MarkerModel(QAbstractListModel):
    PositionRole = Qt.UserRole + 1
    SourceRole = Qt.UserRole + 2
    RotationRole = Qt.UserRole + 3

    _roles = {
        PositionRole: QByteArray(b"position_marker"),
        SourceRole: QByteArray(b"source_marker"),
        RotationRole: QByteArray(b"rotation_marker"),
    }

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._markers = []
        self.vehicle_names = []

    def rowCount(self, index=QModelIndex()):
        return len(self._markers)

    def roleNames(self):
        return self._roles

    def data(self, index, role=Qt.DisplayRole):
        if index.row() >= self.rowCount():
            return QVariant()
        marker = self._markers[index.row()]

        if role == MarkerModel.PositionRole:
            return marker.position_val()
        elif role == MarkerModel.SourceRole:
            return marker.source_val()
        elif role == MarkerModel.RotationRole:
            return marker.rotation_val()
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            marker = self._markers[index.row()]
            if role == MarkerModel.PositionRole:
                marker.setPosition(value)
            elif role == MarkerModel.SourceRole:
                marker.setSource(value)
            elif role == MarkerModel.RotationRole:
                marker.setRotation(value)
            self.dataChanged.emit(index, index)
            return True
        return QAbstractListModel.setData(self, index, value, role)

    def addMarker(self, name, marker):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._markers.append(marker)
        self.endInsertRows()
        self.vehicle_names.append(name)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractListModel.flags(index) | Qt.ItemIsEditable

    def updateMarker(self, name, new_marker):
        if name in self.vehicle_names:
            ind = self.index(self.vehicle_names.index(name), 0)
            self.setData(ind, new_marker.position_val(), MarkerModel.PositionRole)
            self.setData(ind, new_marker.source_val(), MarkerModel.SourceRole)
            self.setData(ind, new_marker.rotation_val(), MarkerModel.RotationRole)

    def removeMarker(self, name):
        row_index = self.vehicle_names.index(name)
        self.beginRemoveRows(QModelIndex(), row_index, row_index)
        del self._markers[row_index]
        self.endRemoveRows()
        self.vehicle_names.remove(name)


class WaypointModel(QAbstractListModel):
    PositionRole = Qt.UserRole + 1
    SourceRole = Qt.UserRole + 2

    _roles = {
        PositionRole: QByteArray(b"waypoint_marker"),
        SourceRole: QByteArray(b"source_waypoint"),
    }

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._waypoints = []
        self.vehicle_names = []

    def rowCount(self, index=QModelIndex()):
        return len(self._waypoints)

    def roleNames(self):
        return self._roles

    def data(self, index, role=Qt.DisplayRole):
        if index.row() >= self.rowCount():
            return QVariant()
        waypoint = self._waypoints[index.row()]

        if role == WaypointModel.PositionRole:
            return waypoint.position_val()
        elif role == WaypointModel.SourceRole:
            return waypoint.source_val()
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():

            waypoint = self._waypoints[index.row()]
            if role == WaypointModel.PositionRole:
                waypoint.setPosition(value)
            elif role == WaypointModel.SourceRole:
                waypoint.setSource(value)
            self.dataChanged.emit(index, index)
            return True
        return QAbstractListModel.setData(self, index, value, role)

    def addWaypoint(self, name, waypoint):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._waypoints.append(waypoint)
        self.endInsertRows()
        self.vehicle_names.append(name)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractListModel.flags(index) | Qt.ItemIsEditable

    def remove_all_waypoint_markers(self):
        self.beginRemoveRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._waypoints = []
        self.endRemoveRows()
        self.vehicle_names.clear()

class FlightLineModel(QAbstractListModel):
    PathRole = Qt.UserRole + 1
    ColorRole = Qt.UserRole + 2

    _roles = {
        PathRole: QByteArray(b"flight_line_path"),
        ColorRole: QByteArray(b"flight_line_color"),
    }

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._pathlines = []
        self.vehicle_names = []

    def rowCount(self, index=QModelIndex()):
        return len(self._pathlines)

    def roleNames(self):
        return self._roles

    def data(self, index, role=Qt.DisplayRole):
        if index.row() >= self.rowCount():
            return QVariant()
        pathline = self._pathlines[index.row()]

        if role == FlightLineModel.PathRole:
            return pathline.path_val()
        elif role == FlightLineModel.ColorRole:
            return pathline.color_val()
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            pathline = self._pathlines[index.row()]
            if role == FlightLineModel.PathRole:
                pathline.setPath(value)
            elif role == FlightLineModel.ColorRole:
                pathline.setColor(value)
            self.dataChanged.emit(index, index)
            return True
        return QAbstractListModel.setData(self, index, value, role)

    def addPathLine(self, name, line):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._pathlines.append(line)
        self.endInsertRows()
        self.vehicle_names.append(name)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractListModel.flags(index) | Qt.ItemIsEditable

    def updatePathLine(self, name, new_line):
        if name in self.vehicle_names:
            ind = self.index(self.vehicle_names.index(name), 0)
            self.setData(ind, new_line.path_val(), FlightLineModel.PathRole)
            self.setData(ind, new_line.color_val(), FlightLineModel.ColorRole)

    def removePathLine(self, name):
        row_index = self.vehicle_names.index(name)
        self.beginRemoveRows(QModelIndex(), row_index, row_index)
        del self._pathlines[row_index]
        self.endRemoveRows()
        self.vehicle_names.remove(name)


class YawLineModel(QAbstractListModel):
    PathRole = Qt.UserRole + 1
    ColorRole = Qt.UserRole + 2

    _roles = {
        PathRole: QByteArray(b"yaw_path"),
        ColorRole: QByteArray(b"yaw_color"),
    }

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._yawlines = []
        self.vehicle_names = []

    def rowCount(self, index=QModelIndex()):
        return len(self._yawlines)

    def roleNames(self):
        return self._roles

    def data(self, index, role=Qt.DisplayRole):
        if index.row() >= self.rowCount():
            return QVariant()
        yawline = self._yawlines[index.row()]

        if role == YawLineModel.PathRole:
            return yawline.path_val()
        elif role == YawLineModel.ColorRole:
            return yawline.color_val()
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            yawline = self._yawlines[index.row()]
            if role == YawLineModel.PathRole:
                yawline.setPath(value)
            elif role == YawLineModel.ColorRole:
                yawline.setColor(value)
            self.dataChanged.emit(index, index)
            return True
        return QAbstractListModel.setData(self, index, value, role)

    def addYawLine(self, name, line):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._yawlines.append(line)
        self.endInsertRows()
        self.vehicle_names.append(name)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractListModel.flags(index) | Qt.ItemIsEditable

    def updateYawLine(self, name, new_line):
        if name in self.vehicle_names:
            ind = self.index(self.vehicle_names.index(name), 0)
            self.setData(ind, new_line.path_val(), YawLineModel.PathRole)
            self.setData(ind, new_line.color_val(), YawLineModel.ColorRole)

    def removeYawLine(self, name):
        row_index = self.vehicle_names.index(name)
        self.beginRemoveRows(QModelIndex(), row_index, row_index)
        del self._yawlines[row_index]
        self.endRemoveRows()
        self.vehicle_names.remove(name)


class HeadingLineModel(QAbstractListModel):
    PathRole = Qt.UserRole + 1
    ColorRole = Qt.UserRole + 2

    _roles = {
        PathRole: QByteArray(b"heading_path"),
        ColorRole: QByteArray(b"heading_color"),
    }

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._headinglines = []
        self.vehicle_names = []

    def rowCount(self, index=QModelIndex()):
        return len(self._headinglines)

    def roleNames(self):
        return self._roles

    def data(self, index, role=Qt.DisplayRole):
        if index.row() >= self.rowCount():
            return QVariant()
        headingline = self._headinglines[index.row()]

        if role == HeadingLineModel.PathRole:
            return headingline.path_val()
        elif role == HeadingLineModel.ColorRole:
            return headingline.color_val()
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            headingline = self._headinglines[index.row()]
            if role == HeadingLineModel.PathRole:
                headingline.setPath(value)
            elif role == HeadingLineModel.ColorRole:
                headingline.setColor(value)
            self.dataChanged.emit(index, index)
            return True
        return QAbstractListModel.setData(self, index, value, role)

    def addHeadingLine(self, name, line):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._headinglines.append(line)
        self.endInsertRows()
        self.vehicle_names.append(name)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractListModel.flags(index) | Qt.ItemIsEditable

    def updateHeadingLine(self, name, new_line):
        if name in self.vehicle_names:
            ind = self.index(self.vehicle_names.index(name), 0)
            self.setData(ind, new_line.path_val(), HeadingLineModel.PathRole)
            self.setData(ind, new_line.color_val(), HeadingLineModel.ColorRole)

    def removeHeadingLine(self, name):
        row_index = self.vehicle_names.index(name)
        self.beginRemoveRows(QModelIndex(), row_index, row_index)
        del self._headinglines[row_index]
        self.endRemoveRows()
        self.vehicle_names.remove(name)


class HomeModel(QAbstractListModel):
    PositionRole = Qt.UserRole + 1
    SourceRole = Qt.UserRole + 2

    _roles = {
        PositionRole: QByteArray(b"position_home"),
        SourceRole: QByteArray(b"source_home"),
    }

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._homes = []
        self.vehicle_names = []

    def rowCount(self, index=QModelIndex()):
        return len(self._homes)

    def roleNames(self):
        return self._roles

    def data(self, index, role=Qt.DisplayRole):
        if index.row() >= self.rowCount():
            return QVariant()
        home = self._homes[index.row()]

        if role == HomeModel.PositionRole:
            return home.position_val()
        elif role == HomeModel.SourceRole:
            return home.source_val()
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            home = self._homes[index.row()]
            if role == HomeModel.PositionRole:
                home.setPosition(value)
            elif role == HomeModel.SourceRole:
                home.setSource(value)
            self.dataChanged.emit(index, index)
            return True
        return QAbstractListModel.setData(self, index, value, role)

    def addHome(self, name, home):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._homes.append(home)
        self.endInsertRows()
        self.vehicle_names.append(name)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractListModel.flags(index) | Qt.ItemIsEditable

    def updateHome(self, name, new_home):
        if name in self.vehicle_names:
            ind = self.index(self.vehicle_names.index(name), 0)
            self.setData(ind, new_home.position_val(), HomeModel.PositionRole)
            self.setData(ind, new_home.source_val(), HomeModel.SourceRole)

    def removeHome(self, name):
        row_index = self.vehicle_names.index(name)
        self.beginRemoveRows(QModelIndex(), row_index, row_index)
        del self._homes[row_index]
        self.endRemoveRows()
        self.vehicle_names.remove(name)


class Marker(QAbstractListModel):
    positionChanged = QtCore.pyqtSignal()
    sourceChanged = QtCore.pyqtSignal(str)
    rotationChanged = QtCore.pyqtSignal(float)

    def __init__(self, parent=None):
        super(Marker, self).__init__(parent)
        self._source = None
        self._position = None
        self._rotation = None

    def position_val(self):
        return self._position

    def setPosition(self, new_pos):
        self._position = new_pos
        self.positionChanged.emit()

    def source_val(self):
        return self._source

    def setSource(self, new_source):
        self._source = new_source
        self.sourceChanged.emit(new_source)

    def rotation_val(self):
        return self._rotation

    def setRotation(self, new_rotation):
        self._rotation = new_rotation
        self.rotationChanged.emit(new_rotation)


class Line(QAbstractListModel):
    pathChanged = QtCore.pyqtSignal(list)
    colorChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(Line, self).__init__(parent)
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

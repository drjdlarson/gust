"""Map Widget for the main frontend window"""
import math
import pathlib
from PyQt5 import (
    QtCore,
    QtPositioning,
    QtQuickWidgets,
)
from PyQt5.QtCore import (
    QTemporaryDir,
    QFile,
    QAbstractListModel,
    Qt,
    QByteArray,
    QModelIndex,
    QVariant,
)


###############
# Main references for dynamically displaying objects on Map::
# 1. QML Maps (https://doc.qt.io/qtforpython-5/overviews/qml-location5-maps.html)
# 2. https://stackoverflow.com/questions/54695976/how-can-i-update-a-qml-objects-property-from-my-python-file
# 3. https://stackoverflow.com/questions/46429800/is-it-possible-to-create-mapquickitems-from-qml-in-python
###############


class MapWidget(QtQuickWidgets.QQuickWidget):
    """Main Map Widget Class. This class is displayed as Promoted Widget in GUST
    Frontend Window"""

    def __init__(self, parent=None):
        super(MapWidget, self).__init__(
            parent,
            resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView,
        )

        # On each of the 3 dicts below, vehicle's name is used as a key.
        # each connected vehicle has a MapHelper Instance as value on _vehicles.
        self._vehicles = {}

        # each vehicle with uploaded missions has a FlightPlanHelper instance as
        # value on _vehicles_mission.
        self._vehicles_mission = {}

        # color of each connected vehicle is saved on _vehicle_color.
        self._vehicle_color = {}

    def setup_qml(self, ctx):
        """Sets up the QML map interface.
        Here, we grab the QML file from the resource folder, make some changes, and
        save the file in some temporary directory. Then, we tell Qt to use that new
        QML file. This renders the map in the frontend. The main thing we are changing
        in the original QML file is specifying the map of offline map.
        Finally, we create attributes for different models (position marker, waypoints,
        home, heading line, yaw line, flight path) in the map."""

        self.ctx = ctx

        # the saved QML file in resources
        qml_file = self.ctx.get_resource("map_widget/map.qml")
        resource_file = self.ctx.get_resource("map_widget/README")
        resource_path = str(pathlib.Path(resource_file).parent.resolve())

        # a new temporary directory
        self.temp_dir = QTemporaryDir()

        # manually updating some strings in the QML file to specify offline_map path
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

            # can copy the new file to a known path (if needed) for debugging.
            # QFile.copy(temp_path + "/temp_map.qml", resource_path + "/from_temp_qml")

        # rendering the map
        self.engine().clearComponentCache()
        self.setSource(QtCore.QUrl.fromLocalFile(temp_path + "/temp_map.qml"))

        # TODO: figure out the qml property for map centering stuff
        self.map_center = self.rootObject().findChild(QtCore.QObject, "center_map")

        # Creating models for QML Map objects and assigning context
        self.marker_model = MarkerModel(self)
        self.rootContext().setContextProperty("markermodel", self.marker_model)

        self.heading_line_model = HeadingLineModel(self)
        self.rootContext().setContextProperty("heading_line", self.heading_line_model)

        self.yaw_line_model = YawLineModel(self)
        self.rootContext().setContextProperty("yaw_line", self.yaw_line_model)

        self.home_model = HomeModel()
        self.rootContext().setContextProperty("homemodel", self.home_model)

        self.flight_path_model = FlightLineModel(self)
        self.rootContext().setContextProperty("flight_line", self.flight_path_model)

        self.waypoint_model = WaypointModel()
        self.rootContext().setContextProperty("waypointmodel", self.waypoint_model)


    def recenter_map(self, center_coordinates):
        """Center the map at the given position.
        Not currently implemented"""
        self.map_center.setProperty(
            "coordinate", QtPositioning.QGeoCoordinate(center_coordinates)
        )

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
        """
        Adds a new vehicle in the map. Each vehicle has an instance of MapHelper.
        This is saved in the _vehicles dict as _vehicle = {name: MapHelper() instance}.
        If the vehicle already exists, it just updates the received parameters, and is
        displayed in the map.

        Parameters
        ----------
        name: str
            Name of the connected vehicle
        color: str
            Predefined color of the connected vehicle
        home_lat: float
            Latitude of the home (deg)
        home_lon: float
            Longitude of the home (deg)
        latitude: float
            Latitude of current position (deg)
        longitude: float
            Longitude of current position (deg)
        yaw: int
            Yaw Angle (deg, psi:Body Frame)
        heading: int
            Heading Angle (deg, sigma:Wind Frame)
        mode: str
            Current Flight mode.

        Returns
        -------

        """

        # for new vehicles
        if name not in self._vehicles:
            # each vehicle has an instance of MapHelper().
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

            # calling function in MapHelper class for the vehicle.
            self._vehicles[name].add_objects_in_map()

        # Just updating the parameters for already connected vehicles.
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
        """
        Display the flight plans in the map with given waypoints.

        Parameters
        ----------
        all_waypoints: dict
            Waypoints information of all connected vehicles.
            {name: list of waypoints}. Each waypoint is a tuple of (Lat, Lon).

        Returns
        -------

        """
        for name, waypoints in all_waypoints.items():
            if name in self._vehicles.keys():
                if name not in self._vehicles_mission.keys():
                    # each vehicle with uploaded mission has an instance of FlightPlanHelper
                    self._vehicles_mission[name] = FlightPlanHelper(
                        name,
                        self._vehicle_color[name],
                        self.waypoint_model,
                        self.flight_path_model,
                        self.ctx,
                    )
                    self._vehicles_mission[name].display_new_mission(waypoints)
                # If the vehicle already exists in _vehicles_mission, just displaying
                # the updated mission with new set of waypoints.
                else:
                    self._vehicles_mission[name].display_updated_mission(waypoints)

    def remove_vehicle_from_map(self, name):
        """Removing the Vehicle's related map elements from the Map."""

        if name in self._vehicles:

            # removing the Position, Yaw, Heading, Home Models
            self._vehicles[name].remove_all_models()
            del self._vehicles[name]
            del self._vehicle_color[name]

            # removing the Waypoints and Flight Path models
            if name in self._vehicles_mission:
                self._vehicles_mission[name].remove_waypoints_and_lines()
                del self._vehicles_mission[name]

class FlightPlanHelper:
    """Helper Class for displaying uploaded flight plans."""

    def __init__(self, name, color, waypoint_model, flight_path_model, ctx):
        self.name = name
        self.color = color
        self.waypoint_model = waypoint_model
        self.flight_path_model = flight_path_model
        self.ctx = ctx

    def remove_waypoints_and_lines(self):
        """Remove mission waypoint and lines from the map"""
        self.flight_path_model.removePathLine(self.name)
        self.waypoint_model.remove_all_waypoint_markers(self.name)

    def display_new_mission(self, waypoints):
        """Display mission waypoint and lines for new vehicles"""

        # prepare waypoint and line to display in the map
        flight_lines, coords = self.prepare_flight_lines_object(waypoints)
        self.flight_path_model.addPathLine(self.name, flight_lines)

        # preparing each waypoint as a marker to display on the map.
        # Have to use the prepare_waypoint_marker_object() for each coordinate unlike
        # a single function for a prepare_flight_lines_object(). This is because
        # flight lines (multiple) is created as a single Line object, whereas waypoints
        # are created as separate Marker objects each.
        for wp_coord in coords:
            wp_marker = self.prepare_waypoint_marker_object(wp_coord)
            self.waypoint_model.addWaypoints(self.name, wp_marker)

    def display_updated_mission(self, new_waypoints):
        """Display mission waypoint and lines for vehicles with new mission"""

        # For flight lines, we can just update the lines.
        new_flight_lines, coords = self.prepare_flight_lines_object(new_waypoints)
        self.flight_path_model.updatePathLine(self.name, new_flight_lines)

        # For waypoint markers, we have to remove the waypoint markers and redraw them
        self.waypoint_model.remove_all_waypoint_markers(self.name)
        for wp_coord in coords:
            wp_marker = self.prepare_waypoint_marker_object(wp_coord)
            self.waypoint_model.addWaypoints(self.name, wp_marker)

    def prepare_waypoint_marker_object(self, wp_coord):
        """Prepares waypoint marker objects for the set waypoints."""

        # each vehicle's set of waypoints are a separate instance of Marker class.
        wp_marker = Marker()

        # selecting appropriate color waypoint icon from the resources..
        file = "map_widget/colored_icons/" + self.color + "_waypoint.png"
        icon_type = self.ctx.get_resource(file)
        wp_marker.setSource(icon_type)
        wp_marker.setPosition(wp_coord)
        return wp_marker

    def prepare_flight_lines_object(self, waypoints):
        """Prepares flight lines objects for the set waypoints."""

        # each vehicle's set of flight plan lines are a separate instance of Line class.
        flight_lines = Line()
        flight_lines.setColor(self.color)

        # setting each coordinate as a QGeoCoordinate object.
        qcoordinates = [QtPositioning.QGeoCoordinate(*ii) for ii in waypoints]
        flight_lines.setPath(qcoordinates)
        return flight_lines, qcoordinates


class MapHelper:
    """Helper Class for displaying vehicle's position in the map"""

    # Each vehicle should have an instance of this class with all arguments of the
    # __init__() function.

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
        """Removes all models of map elements for the vehicle from the map"""
        self.marker_model.removeMarker(self.name)
        self.yaw_model.removeYawLine(self.name)
        self.heading_model.removeHeadingLine(self.name)
        self.home_model.removeHome(self.name)

    def add_objects_in_map(self):
        """Add the map elements for new vehicle on the map"""
        self.marker_model.addMarker(self.name, self.prepare_marker_object())
        self.yaw_model.addYawLine(
            self.name, self.prepare_line_object("white", self.yaw)
        )
        self.heading_model.addHeadingLine(
            self.name, self.prepare_line_object("black", self.heading)
        )
        self.home_model.addHome(self.name, self.prepare_home_object())

    def update_objects_in_map(self):
        """Update the map elements for existing vehicles on tha map"""
        self.marker_model.updateMarker(self.name, self.prepare_marker_object())
        self.yaw_model.updateYawLine(
            self.name, self.prepare_line_object("white", self.yaw)
        )
        self.heading_model.updateHeadingLine(
            self.name, self.prepare_line_object("black", self.heading)
        )
        self.home_model.updateHome(self.name, self.prepare_home_object())

    def prepare_line_object(self, color, angle):
        """
        Prepare Line Object for display in map. Used for Heading line, yaw line, etc.

        Parameters
        ----------
        color: str
            color for the line
        angle: int
            bearing for the line

        Returns
        -------

        """
        line = Line()
        line.setColor(color)

        # 2nd coordinate for the line based on 1st coordinate and an angle
        coordinates = [
            (self.latitude, self.longitude),
            self.get_points(angle),
        ]
        # preparing each coordinate as a QGeoCoordinate object
        qcoordinates = [QtPositioning.QGeoCoordinate(*ii) for ii in coordinates]
        line.setPath(qcoordinates)
        return line

    def prepare_home_object(self):
        """Prepares Home marker object based on home location coordinates"""
        home = Marker()
        # selecting appropriate color icon for home from the resources
        file = "map_widget/colored_icons/" + self.color + "_home.png"
        home.setSource(self.ctx.get_resource(file))
        home_pos = (self.home_lat, self.home_lon)
        # preparing the home coordinate as a QGeoCoordinate object
        home_pos_coord = QtPositioning.QGeoCoordinate(*home_pos)
        home.setPosition(home_pos_coord)
        return home

    def prepare_marker_object(self):
        """Prepares position marker object based on current position coordinates.
        Similar to prepare_home_objects()"""
        marker = Marker()
        marker.setSource(self.drone_icon_selector())
        marker.setRotation(self.yaw)
        pos = (self.latitude, self.longitude)
        pos_coord = QtPositioning.QGeoCoordinate(*pos)
        marker.setPosition(pos_coord)
        return marker

    def get_points(self, angle):
        """
        Get the 2nd coordinate based on current location and a bearing.
        This is used to find the 2nd coordinate of a display line for heading, yaw, etc.
        Uses Haversine Equations.

        Currently, this is fixed to be 1 km, but this can be set to be dynamic.

        Parameters
        ----------
        angle: int
            Bearing of the line from current position

        Returns
        -------
        (Lat, Lon) for the 2nd coordinate

        """

        # radius of earth (in km)
        R = 6378.1
        # length of line (fixed as 1km for now)
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
        """Selects icon based on current flight mode"""

        # The colored icons for different modes are saved in resources.
        if self.mode == "stabilize".upper():
            file = "map_widget/colored_icons/" + self.color + "_pos.png"
            icon_type = self.ctx.get_resource(file)
        elif self.mode == "rtl".upper():
            file = "map_widget/colored_icons/" + self.color + "_rtl_pos.png"
            icon_type = self.ctx.get_resource(file)
        else:
            file = "map_widget/colored_icons/" + self.color + "_spos.png"
            icon_type = self.ctx.get_resource(file)
        return icon_type


class MarkerModel(QAbstractListModel):
    """A Map element to display Position of vehicle on the map"""

    # Each vehicle has only one Marker object.

    PositionRole = Qt.UserRole + 1
    SourceRole = Qt.UserRole + 2
    RotationRole = Qt.UserRole + 3

    # Assigning context to model variables in QML (See map.qml in resources)
    _roles = {
        PositionRole: QByteArray(b"position_marker"),
        SourceRole: QByteArray(b"source_marker"),
        RotationRole: QByteArray(b"rotation_marker"),
    }

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)

        # Each item in _markers and vehicle_names represent a vehicle connected.
        self._markers = []
        self.vehicle_names = []

    def rowCount(self, index=QModelIndex()):
        """Returns the size of _markers list.
        Each item in the list corresponds to each vehicle"""
        return len(self._markers)

    def roleNames(self):
        """Returns the roles defined in the class"""
        return self._roles

    def data(self, index, role=Qt.DisplayRole):
        """Get the current data of the required index (in _markers) and role (in _roles)."""
        if index.row() >= self.rowCount():
            return QVariant()

        # Find the marker object stored in selected index of _markers.
        marker = self._markers[index.row()]

        # Find the current value of respective roles.
        if role == MarkerModel.PositionRole:
            return marker.position_val()
        elif role == MarkerModel.SourceRole:
            return marker.source_val()
        elif role == MarkerModel.RotationRole:
            return marker.rotation_val()
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        """Set the value of the required index (in _markers) and role (in _roles)"""
        if index.isValid():

            # Find the marker object stores in selected index of _markers
            marker = self._markers[index.row()]

            # Set the current value of respective roles
            if role == MarkerModel.PositionRole:
                marker.setPosition(value)
            elif role == MarkerModel.SourceRole:
                marker.setSource(value)
            elif role == MarkerModel.RotationRole:
                marker.setRotation(value)

            # Emit a signal to notify that the value of some parameter has changed
            self.dataChanged.emit(index, index)
            return True

        return QAbstractListModel.setData(self, index, value, role)

    def addMarker(self, name, marker):
        """Add a new marker in the map"""

        # Telling QML that we're adding a new element in the same object.
        # i.e. adding a new item in the list of _markers. Also need to specify current
        # length of rows and tell when the process is completed.
        #
        # Note: we are adding a single element here, so we are using same index as
        # arguments in beginInsertRows()
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._markers.append(marker)
        self.endInsertRows()

        # Adding the vehicle's name in a separate list with the same index as in _markers.
        # This was necessary because the specific marker object in _markers can be only
        # accessed by its index. Adding the vehicle's name in a separate list allows
        # to easily find the index for that vehicle. This index is used to find the
        # marker's object in _markers. (See updateMarker() below.)
        self.vehicle_names.append(name)

    def flags(self, index):
        """Send some flag if the index is not found in _markers."""
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractListModel.flags(index) | Qt.ItemIsEditable

    def updateMarker(self, name, new_marker):
        """Update the marker with a new marker object"""

        if name in self.vehicle_names:

            # finding the index of the vehicle's marker object.
            # this is done indirectly by finding the index of vehicle's name in
            # vehicle_names list.
            ind = self.index(self.vehicle_names.index(name), 0)

            # Setting a new value for each role of the object in that index
            self.setData(ind, new_marker.position_val(), MarkerModel.PositionRole)
            self.setData(ind, new_marker.source_val(), MarkerModel.SourceRole)
            self.setData(ind, new_marker.rotation_val(), MarkerModel.RotationRole)

    def removeMarker(self, name):
        """Removes the marker object from the map"""

        # Finding the index of vehicle's name in vehicle_names
        row_index = self.vehicle_names.index(name)

        # Telling QML that we're removing items from _markers.
        self.beginRemoveRows(QModelIndex(), row_index, row_index)
        del self._markers[row_index]
        self.endRemoveRows()
        self.vehicle_names.remove(name)


class WaypointModel(QAbstractListModel):
    """A Map element to display waypoints of vehicle's mission on the map"""

    # Similar to MarkerModel class mostly (See MarkerModel class above).

    # Difference from MarkerModel Class:::
    # Since each waypoint is a separate Marker object in _waypoints, there
    # are multiple waypoint Marker objects for each vehicle. So there are multiple
    # "name" items in the vehicle_names for each vehicle.

    # Every time a new set of mission waypoints is received, all waypoints are removed
    # and redrawn. This is done in FlightPathHelper.display_updated_mission().

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

    def addWaypoints(self, name, waypoint):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._waypoints.append(waypoint)
        self.endInsertRows()
        self.vehicle_names.append(name)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractListModel.flags(index) | Qt.ItemIsEditable

    def remove_all_waypoint_markers(self, name):

        # Finding the indices of all items with the vehicle's name
        indices = [ind for ind, ele in enumerate(self.vehicle_names) if ele == name]

        # deleting all objects relating to the vehicle.
        for i in sorted(indices, reverse=True):
            self.beginRemoveRows(QModelIndex(), i, i)
            del self._waypoints[i]
            del self.vehicle_names[i]
            self.endRemoveRows()


class FlightLineModel(QAbstractListModel):
    """A Map element to display flight lines of vehicle's mission on the map"""

    # Similar to MarkerModel class (see above).

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
    """A Map element to display Yaw direction (line) of vehicle on the map"""

    # Similar to MarkerModel class (see above).

    # Direction between Nav Frame and Body Frame (psi) following DrJDL's convention.

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
    """A Map element to display heading direction (line) of vehicle on the map"""

    # Similar to MarkerModel class (see above).

    # Direction between Nav Frame and Wind frame (sigma) following DrJDL's convention.

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
    """A Map element to display position of Home of vehicle on the map"""

    # Similar to MarkerModel class (see above).

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
    """A helper class to create marker objects in the Map"""

    # signals to notify that the item's value is changed
    positionChanged = QtCore.pyqtSignal()
    sourceChanged = QtCore.pyqtSignal(str)
    rotationChanged = QtCore.pyqtSignal(float)

    def __init__(self, parent=None):
        super(Marker, self).__init__(parent)
        self._source = None
        self._position = None
        self._rotation = None

    def position_val(self):
        """Returns the current position value"""
        return self._position

    def setPosition(self, new_pos):
        """
        Change the position of the object to new_pos

        Parameters
        ----------
        new_pos: QGeoCoordinate object
            (Lat, Lon) formatted as QGeoCoordinate object
            (See MapHelper.prepare_marker_object().)

        Returns
        -------

        """
        self._position = new_pos
        # emit the signal once the value is changed
        self.positionChanged.emit()

    def source_val(self):
        """Returns the current source for icon"""
        return self._source

    def setSource(self, new_source):
        """
        Change the source of icon to new_source

        Parameters
        ----------
        new_source: str
            File path of new icon.

        Returns
        -------

        """
        self._source = new_source
        self.sourceChanged.emit(new_source)

    def rotation_val(self):
        """Returns the current value of bearing angle."""
        return self._rotation

    def setRotation(self, new_rotation):
        """
        Change the bearing of the object to new_rotation

        Parameters
        ----------
        new_rotation: int
            New bearing for the object

        Returns
        -------

        """
        self._rotation = new_rotation
        self.rotationChanged.emit(new_rotation)


class Line(QAbstractListModel):
    """A helper class to create Lines in the map"""

    # Similar to Marker class (see above.)

    pathChanged = QtCore.pyqtSignal(list)
    colorChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(Line, self).__init__(parent)
        self._color = "black"
        self._path = None

    def color_val(self):
        return self._color

    def setColor(self, new_color):
        """
        Set the color of the object to new_color

        Parameters
        ----------
        new_color: str
            Color for the object (See list of QML available colors.)

        Returns
        -------

        """
        self._color = new_color
        self.colorChanged.emit(new_color)

    def path_val(self):
        return self._path

    def setPath(self, new_path):
        """
        Set the path of new line to new_path

        Parameters
        ----------
        new_path: list
            A list of QGeoCoordinate objects. (See MapHelper.prepare_line_object().)

        Returns
        -------

        """
        self._path = new_path
        self.pathChanged.emit(new_path)

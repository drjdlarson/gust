"""Map Widget for all planning windows"""

import pathlib
from PyQt5 import QtCore, QtPositioning, QtQuickWidgets
from PyQt5.QtCore import QTemporaryDir, QFile, QAbstractListModel, Qt, QByteArray, QModelIndex, QVariant


class PlanningMapWidget(QtQuickWidgets.QQuickWidget):
    """Main Map widget cals for all Planning Windows"""

    # Similar to MapWidget class (See gust.gui.ui.map_widget.py)

    def __init__(self, parent=None):
        super(PlanningMapWidget, self).__init__(parent,
                                                resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        self._grid_line_names = []
        self._waypoint_line_names = []

    def setup_qml(self, ctx):
        """Sets up the QML map interface. See MapWidget.setup_qml() for more."""

        self.ctx = ctx
        qml_file = self.ctx.get_resource("cmr_planning/planning_map.qml")
        resource_file = self.ctx.get_resource('map_widget/README')
        resource_path = str(pathlib.Path(resource_file).parent.resolve())

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

        self.line_model = LineModel()
        self.rootContext().setContextProperty("line_model", self.line_model)

    def change_grid_line_state(self, val):
        """Change the visibility of grid lines on the map."""

        if self._grid_line_names:
            if val == 1:
                self.line_model.change_line_color("yellow_grid", "yellow")
            else:
                self.line_model.change_line_color("yellow_grid", "transparent")

                
    def change_waypoints_line_state(self, val, wpcolor=None):
        """
        Change the visibility of flight path lines on the map

        Parameters
        ----------
        val : int (0 or 1)
            1 will make it visible, 0 will hide the line
        wpcolor : str (optional)
            Color associated with the waypoints
            If wpcolor is not provided, visibility is changed to val for all
            waypoints (example: CMR planning window).

        Returns
        -------

        """

        if wpcolor is None:
            if self._waypoint_line_names:
                for name in self._waypoint_line_names:
                    color = name.split("_")[0]
                    self.change_waypoints_visibility(name, color, val)

        # Changing visibility for individual plans
        else:
            model_name = self.form_line_model_name(wpcolor)
            self.change_waypoints_visibility(model_name, wpcolor, val)

    def change_waypoints_visibility(self, name, color, val):
        """Change the visibility of waypoint model to val"""
        if val == 1:
            self.line_model.change_line_color(name, color)
        else:
            self.line_model.change_line_color(name, "transparent")


    def add_grid_lines(self, coordinates):
        """
        Add Grid lines on the map

        For CMR, this is shown as the Line-of-Interest. This may not be used for normal
        flight planning. This is yellow in color.

        Parameters
        ----------
        coordinates: list
            List of coordinates in the format (Lat, Lon)

        Returns
        -------

        """

        # Creating and adding lines is done similar to MapWidget.
        grid_line = Lines()
        grid_line.setColor("yellow")
        qcoordinates = [QtPositioning.QGeoCoordinate(*ii) for ii in coordinates]
        grid_line.setPath(qcoordinates)
        self.line_model.addLine("yellow_grid", grid_line)
        self._grid_line_names.append("yellow_grid")

    def add_waypoint_lines(self, coordinates, color):
        """
        Add vehicle's flight plan on the map.

        Parameters
        ----------
        coordinates: list
            List of mission's waypoint coordinates in the form (Lat. Lon)
        color: str
            Color associated with the vehicle

        Returns
        -------

        """

        # Creating and adding lines is done similar to MapWidget
        wp_line = Lines()
        wp_line.setColor(color)
        qcoordinates = [QtPositioning.QGeoCoordinate(*ii) for ii in coordinates]
        wp_line.setPath(qcoordinates)
        self.line_model.addLine(self.form_line_model_name(color), wp_line)
        self._waypoint_line_names.append(self.form_line_model_name(color))

    def remove_line_from_map(self, wpcolor):
        """Removes the line models associated with the color"""
        self.line_model.remove_line(self.form_line_model_name(wpcolor))

    def form_line_model_name(self, color):
        """Returns string 'color_name'."""
        return "{}_wp".format(color)


class Lines(QAbstractListModel):
    """A helper class to create lines in the map"""

    # Similar to Line class in gust.gui.ui.map_widget.py

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
    """A Map element to display flight lines of vehicle's mission on the map"""

    # Similar to FlightLineModel class in gust.gui.ui.map_widget.py

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

    def remove_line(self, name):
        row_index = self.object_names.index(name)
        self.beginRemoveRows(QModelIndex(), row_index, row_index)
        del self._lines[row_index]
        self.endRemoveRows()
        self.object_names.remove(name)

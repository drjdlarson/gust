import os, time, random
from PyQt5 import QtCore, QtWidgets, QtQuickWidgets, QtPositioning, QtQuickWidgets

class MarkerModel(QtCore.QAbstractListModel):
    PositionRole, SourceRole = range(QtCore.Qt.UserRole, QtCore.Qt.UserRole + 2)

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
        return QtCore.QVariant()

    def roleNames(self):
        return {MarkerModel.PositionRole: b"position_marker", MarkerModel.SourceRole: b"source_marker"}

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

class MapWidget(QtQuickWidgets.QQuickWidget):
    def __init__(self, parent=None):
        super(MapWidget, self).__init__(parent,
            resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView)

        self.model = MarkerModel(self)
        self.rootContext().setContextProperty("markermodel", self.model)

        qml_path = os.path.join(os.path.dirname(__file__), "map.qml")
        self.setSource(QtCore.QUrl.fromLocalFile(qml_path))
        self.url = "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png"

        self.timer = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
        self.timer.timeout.connect(self.add_drone)
        self.timer2.timeout.connect(self.clear_drones)
        self.timer.start(1000)
        self.timer2.start(1000)


    def add_drone(self):
        lat = 44.97104 + round(random.uniform(0.01, 0.09), 2)
        lon = -93.46055 + round(random.uniform(0.01, 0.09), 2)
        pos = (lat, lon)
        coord = QtPositioning.QGeoCoordinate(*pos)
        source = QtCore.QUrl(self.url)
        self.model.appendMarker({"position": coord, "source": source})

    def clear_drones(self):
        print("clearing")
        self.model.remove_marker()


if __name__ == '__main__':

    first_lat = 44.97104
    first_lon = -93.46055
    positions = []
    # making fake lat luong
    for i in range(10):
        new_lat = first_lat + i * 10 ** -2
        new_lon = first_lon + i * 10 ** -2
        positions.append((new_lat, new_lon))

    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MapWidget()
    w.show()


    sys.exit(app.exec_())

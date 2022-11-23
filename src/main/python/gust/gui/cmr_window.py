"""Logic for CMR planning window"""
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QCheckBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QAbstractListModel, Qt, QByteArray

from gust.gui.ui.cmr_window import Ui_MainWindow

# TODO: Replace the Test Class and fix file paths to use ctx

# %%
class CmrWindow(QMainWindow, Ui_MainWindow):
    """Main interface for the CMR Planning window"""

    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)

        self._grid_line_added = False
        self._waypoints_line_added = False

        self.ctx = ctx
        self.setupUi(self)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        self.setPalette(self.parentWidget().palette())

        pixmap = QPixmap(self.ctx.get_resource('cmr_planning/cmr_schematic.jpeg'))
        self.label_schematic.setPixmap(pixmap)

        self.widget_cmr_map.setup_qml(self.ctx)

# %%

# *** ONLY FOR TESTING ***
class TestCmrWindow(QMainWindow, Ui_MainWindow):
    """Test interface for the CMR Planning window"""

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.pushButton_draw_grid.clicked.connect(self.clicked_draw_grid)
        self.pushButton_generate_wp.clicked.connect(self.clicked_generate_waypoints)
        self.pushButton_load_wp.clicked.connect(self.clicked_load_waypoints)

        self.checkBox_grid.stateChanged.connect(self.grid_checkbox_changed)

    def clicked_load_waypoints(self):
        pass


    def clicked_generate_waypoints(self):
        waypoints = {}

        dummy_wp1 = [(33.13514, -87.1241241), (32.23414, -86.324241), (33.63514, -87.31441241)]
        dummy_wp2 = [(33.736514, -86.1241241), (32.154135, -86.6474241), (32.63514, -87.141241)]

        waypoints.update({1: {'coordinates': dummy_wp1, 'color': 'red'}})
        waypoints.update({2: {'coordinates': dummy_wp2, 'color': 'blue'}})

        self.widget_cmr_map.display_waypoint_lines(waypoints[1]['coordinates'], waypoints[1]['color'])
        self.widget_cmr_map.display_waypoint_lines(waypoints[2]['coordinates'], waypoints[2]['color'])

        self.checkboxes = {}
        for key, value in waypoints.items():
            color = value['color']
            self.checkboxes.update({color: QCheckBox()})
            self.checkboxes[color].setText(color)
            self.checkboxes[color].setChecked(True)
            self.horizontalLayout_checkboxes.addWidget(self.checkboxes[color])
        self.widget_cmr_map.clear_grid_lines()


    def clicked_draw_grid(self):
        """
        FOR NOW, JUST DOING ONE LINE.
        Calculates the coordinates of the grid lines

        Returns
        -------
        None.

        """

        grid_points = []
        grid_points.append((float(self.lineEdit_start_lat.text()),
                            float(self.lineEdit_start_lon.text())))
        grid_points.append((float(self.lineEdit_end_lat.text()),
                            float(self.lineEdit_end_lon.text())))

        self.widget_cmr_map.display_grid_lines(grid_points)
        self.checkBox_grid.setChecked(True)

    def grid_checkbox_changed(self):
        pass

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)

        # use ctx after done with Test Class.
        rsrc_path = '/home/lagerprocessor/Projects/gust/src/main/resources/base/cmr_planning/'
        pixmap = QPixmap(rsrc_path + 'cmr_schematic.jpeg')
        self.label_schematic.setPixmap(pixmap)

        self.widget_cmr_map.setup_qml_for_test(rsrc_path)
        self.set_default_values()

    def set_default_values(self):
        self.lineEdit_grid_spacing.setText(str(100))
        self.lineEdit_start_lat.setText(str(33.223245))
        self.lineEdit_start_lon.setText(str(-87.532507))
        self.lineEdit_end_lat.setText(str(33.209869))
        self.lineEdit_end_lon.setText(str(-87.546285))
        self.lineEdit_rel_height.setText(str(75))
        self.lineEdit_spacing.setText(str(25))
        self.lineEdit_theta_max.setText(str(60))
        self.lineEdit_theta_min.setText(str(15))

if __name__ == "__main__":

    import sys
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    w = TestCmrWindow()

    w.show()
    sys.exit(app.exec_())

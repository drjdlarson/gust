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
        self.checkBox_waypoints.stateChanged.connect(self.waypoints_checkbox_changed)

    def clicked_load_waypoints(self):
        pass

    def clicked_generate_waypoints(self):
        waypoints = {}

        dummy_wp1 = [(33.21589373771255, -87.56986696619138),
                     (33.19992239477393, -87.54676703331124),
                     (33.218759762150036, -87.512328099724)]
        dummy_wp2 = [(33.209829960064916, -87.5773701534723),
                     (33.21101600187825, -87.51407923194029),
                     (33.19971306791958, -87.55377156217645)]

        waypoints.update({1: {'coordinates': dummy_wp1, 'color': 'red'}})
        waypoints.update({2: {'coordinates': dummy_wp2, 'color': 'blue'}})

        self.widget_cmr_map.add_waypoint_lines(dummy_wp1 , "blue")
        self.widget_cmr_map.add_waypoint_lines(dummy_wp2, 'red')
        self.checkBox_waypoints.setCheckState(True)

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

        self.widget_cmr_map.add_grid_lines(grid_points)
        self.checkBox_grid.setChecked(True)

    def grid_checkbox_changed(self):
        if self.checkBox_grid.isChecked() == True:
            self.widget_cmr_map.change_grid_line_state(1)
        else:
            self.widget_cmr_map.change_grid_line_state(0)

    def waypoints_checkbox_changed(self):
        if self.checkBox_waypoints.isChecked() == True:
            self.widget_cmr_map.change_waypoints_line_state(1)
        else:
            self.widget_cmr_map.change_waypoints_line_state(0)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)

        # use ctx after done with Test Class.
        rsrc_path = '/home/lagerprocessor/Projects/gust/src/main/resources/base/cmr_planning/'
        pixmap = QPixmap(rsrc_path + 'cmr_schematic.jpeg')
        self.label_schematic.setPixmap(pixmap)

        self.checkBox_waypoints.setTristate(False)
        self.checkBox_grid.setTristate(False)

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

"""Logic for zed manager/viewer window."""
import requests
import pyqtgraph as pg
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer
from ruamel.yaml import YAML

from zed import ConfigSet
from gust.gui.ui.zed_window import Ui_ZedWindow
from wsgi_apps.api.url_bases import BASE, ZED

URL_BASE = "http://localhost:8000/{}/{}/".format(BASE, ZED)
yaml = YAML()


class ZedWindow(QMainWindow, Ui_ZedWindow):
    """Main interface for the sensors selection window"""

    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)
        self.config = ConfigSet()
        self.timer = None
        self._plot_rate = 1.0
        self.update_rate = 1.0

        opts = dict(size=10, brush=pg.mkBrush(255, 255, 255, 120))
        self.top_ax = None
        self.top_data = pg.ScatterPlotItem(**opts)
        self.front_ax = None
        self.front_data = pg.ScatterPlotItem(**opts)
        self.left_ax = None
        self.left_data = pg.ScatterPlotItem(**opts)
        # self.ax3d = None
        # self.data3d = None

        self.setupUi(self)

        self.action_Open_configuration.triggered.connect(self.load_config)

        self.pushButton_connect.clicked.connect(self.connect_clicked)
        self.pushButton_reset.clicked.connect(self.reset_clicked)

        self.lineEdit_id.textChanged.connect(self.id_changed)
        self.lineEdit_name.textChanged.connect(self.name_changed)
        self.lineEdit_locx.textChanged.connect(self.loc_changed(0, self.lineEdit_locx))
        self.lineEdit_locy.textChanged.connect(self.loc_changed(1, self.lineEdit_locy))
        self.lineEdit_locz.textChanged.connect(self.loc_changed(2, self.lineEdit_locz))
        self.lineEdit_dcm00.textChanged.connect(self.dcm_changed(0, 0, self.lineEdit_dcm00))
        self.lineEdit_dcm01.textChanged.connect(self.dcm_changed(0, 1, self.lineEdit_dcm01))
        self.lineEdit_dcm02.textChanged.connect(self.dcm_changed(0, 2, self.lineEdit_dcm02))
        self.lineEdit_dcm10.textChanged.connect(self.dcm_changed(1, 0, self.lineEdit_dcm10))
        self.lineEdit_dcm11.textChanged.connect(self.dcm_changed(1, 1, self.lineEdit_dcm11))
        self.lineEdit_dcm12.textChanged.connect(self.dcm_changed(1, 2, self.lineEdit_dcm12))
        self.lineEdit_dcm20.textChanged.connect(self.dcm_changed(2, 0, self.lineEdit_dcm20))
        self.lineEdit_dcm21.textChanged.connect(self.dcm_changed(2, 1, self.lineEdit_dcm21))
        self.lineEdit_dcm22.textChanged.connect(self.dcm_changed(2, 2, self.lineEdit_dcm22))
        self.lineEdit_minx.textChanged.connect(self.min_changed(0, self.lineEdit_minx))
        self.lineEdit_miny.textChanged.connect(self.min_changed(1, self.lineEdit_miny))
        self.lineEdit_minz.textChanged.connect(self.min_changed(2, self.lineEdit_minz))
        self.lineEdit_maxx.textChanged.connect(self.max_changed(0, self.lineEdit_maxx))
        self.lineEdit_maxy.textChanged.connect(self.max_changed(1, self.lineEdit_maxy))
        self.lineEdit_maxz.textChanged.connect(self.max_changed(2, self.lineEdit_maxz))
        self.lineEdit_plot_rate.textChanged.connect(self.plot_rate_changed)
        self.lineEdit_update_rate.textChanged.connect(self.update_rate_changed)

        self.lineEdit_update_rate.setText(str(self.update_rate))
        self.lineEdit_plot_rate.setText(str(self._plot_rate))

    @property
    def plot_rate_ms(self):
        # protect against division by 0
        if abs(self._plot_rate) < 1e-5:
            return 1e3
        return 1.0 / abs(self._plot_rate) * 1e3

    def reset_config_line_edits(self):
        self.config.id = -1
        self.lineEdit_id.setText("")
        self.lineEdit_name.setText("")

        self.lineEdit_locx.setText("")
        self.lineEdit_locy.setText("")
        self.lineEdit_locz.setText("")

        self.lineEdit_dcm00.setText("")
        self.lineEdit_dcm01.setText("")
        self.lineEdit_dcm02.setText("")
        self.lineEdit_dcm10.setText("")
        self.lineEdit_dcm11.setText("")
        self.lineEdit_dcm12.setText("")
        self.lineEdit_dcm20.setText("")
        self.lineEdit_dcm21.setText("")
        self.lineEdit_dcm22.setText("")

        self.lineEdit_minx.setText("")
        self.lineEdit_miny.setText("")
        self.lineEdit_minz.setText("")

        self.lineEdit_maxx.setText("")
        self.lineEdit_maxy.setText("")
        self.lineEdit_maxz.setText("")

        self.lineEdit_conf.setText("")
        self.lineEdit_tex_conf.setText("")

        self.checkBox_req_cal.setCheckState(False)

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)
        self.setPalette(self.parentWidget().palette())

        self.reset_config_line_edits()

        x_cage_lims = (0, 10)
        y_cage_lims = (0, 7)
        z_cage_lims = (0, 4)

        # self.ax3d = self.widget_graphs.addPlot(row=0, col=0)
        self.top_ax = self.widget_graphs.addPlot(row=0, col=1)
        self.left_ax = self.widget_graphs.addPlot(row=1, col=0)
        self.front_ax = self.widget_graphs.addPlot(row=1, col=1)

        self.top_ax.addItem(self.top_data)
        self.top_ax.setTitle("Top Down View")
        self.top_ax.setLabel("bottom", "X (m)")
        self.top_ax.setLabel("left", "Y (m)")
        self.top_ax.setXRange(x_cage_lims[0], x_cage_lims[1], padding=0)
        self.top_ax.setYRange(y_cage_lims[0], y_cage_lims[1], padding=0)

        self.left_ax.addItem(self.left_data)
        self.left_ax.setTitle("Left Side View")
        self.left_ax.setLabel("bottom", "Y (m)")
        self.left_ax.setLabel("left", "Z (m)")
        self.left_ax.setXRange(y_cage_lims[0], y_cage_lims[1], padding=0)
        self.left_ax.setYRange(z_cage_lims[0], z_cage_lims[1], padding=0)

        self.front_ax.addItem(self.front_data)
        self.front_ax.setTitle("Front View")
        self.front_ax.setLabel("bottom", "X (m)")
        self.front_ax.setLabel("left", "Z (m)")
        self.front_ax.setXRange(x_cage_lims[0], x_cage_lims[1], padding=0)
        self.front_ax.setYRange(z_cage_lims[0], z_cage_lims[1], padding=0)

    def update_plot_data(self):
        url = "{}get_current_points".format(URL_BASE)
        resp = requests.get(url).json()
        x = resp['xpos']
        y = resp['ypos']
        z = resp['zpos']

        self.top_data.setData(x, y)
        self.left_data.setData(y, z)
        self.front_data.setData(x, z)

        self.timer.start(self.plot_rate_ms)

    def connect_clicked(self):
        url = "{}connect?".format(URL_BASE)
        url += "id={}&name={}&".format(
            self.config.id, self.config.name.replace(" ", "_")
        )
        url += "locx={}&locy={}&locz={}&".format(
            self.config.loc[0], self.config.loc[1], self.config.loc[2]
        )
        for row in range(3):
            for col in range(3):
                url += "dcm{}{}={}&".format(row, col, self.config.dcm[row, col])
        url += "minx={}&miny={}&minz={}&".format(self.config.min[0], self.config.min[1], self.config.min[2])
        url += "maxx={}&maxy={}&maxz={}&".format(self.config.max[0], self.config.max[1], self.config.max[2])
        url += "conf={}&tex_conf={}&".format(self.config.conf, self.config.tex_conf)
        url += "updateHz={}".format(self.update_rate)

        resp = requests.get(url).json()

        dlg = QMessageBox(parent=self)
        if resp["success"]:
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.setText("Connected to ZED!")
            dlg.setWindowTitle("Success!")

        else:
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.setText("Failed to connect to ZED!")
            dlg.setWindowTitle("Failed!")
            dlg.setDetailedText(resp["msg"])

        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        dlg.exec_()

        if resp["success"] and self.timer is None:
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_plot_data)
            self.timer.start(self.plot_rate_ms)

    def reset_clicked(self):
        self.config = ConfigSet()
        self.reset_config_line_edits()


    def plot_rate_changed(self, e):
        try:
            v = float(self.lineEdit_plot_rate.text())
        except ValueError:
            return
        self._plot_rate = v

    def update_rate_changed(self, e):
        try:
            v = float(self.lineEdit_plot_rate.text())
        except ValueError:
            return
        self.update_rate = v

    def id_changed(self, e):
        try:
            new_id = int(self.lineEdit_id.text())
        except ValueError:
            return
        self.config.id = new_id

    def name_changed(self, e):
        self.config.name = self.lineEdit_name.text()

    def loc_changed(self, ind, le):
        def f(e):
            try:
                v = float(le.text())
            except ValueError:
                return
            self.config.loc[ind] = v
        return f

    def min_changed(self, ind, le):
        def f(e):
            try:
                v = float(le.text())
            except ValueError:
                return
            self.config.min[ind] = v
        return f

    def max_changed(self, ind, le):
        def f(e):
            try:
                v = float(le.text())
            except ValueError:
                return
            self.config.max[ind] = v
        return f

    def dcm_changed(self, row, col, le):
        def f(e):
            try:
                v = float(le.text())
            except ValueError:
                return
            self.config.dcm[row, col] = v
        return f

    def conf_changed(self, e):
        try:
            v = int(self.lineEdit_conf.text())
        except ValueError:
            return
        self.config.conf = v

    def tex_conf_changed(self, e):
        try:
            v = int(self.lineEdit_tex_conf.text())
        except ValueError:
            return
        self.config.tex_conf = v

    def load_config(self):
        # open file dialog
        dlg = QFileDialog(caption="Select ZED Configuration File", parent=self)
        dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
        dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dlg.setNameFilters(["Config files (*.yaml)", "All files (*.*)"])

        if dlg.exec_():
            filename = dlg.selectedFiles()[0]
        else:
            return

        # parse config file
        with open(filename, "r") as fin:
            config = yaml.load(fin)

        self.reset_config_line_edits()

        # set all line edits based on parsed config file
        uid = list(config.keys())[0]
        self.lineEdit_id.setText(uid)

        params = config[uid]
        self.lineEdit_name.setText(params["friendly_name"])
        self.lineEdit_locx.setText(str(params["sense_loc_in_world"][0]))
        self.lineEdit_locy.setText(str(params["sense_loc_in_world"][1]))
        self.lineEdit_locz.setText(str(params["sense_loc_in_world"][2]))

        self.lineEdit_dcm00.setText(str(params["dcm_sense2world"]["row_1"][0]))
        self.lineEdit_dcm01.setText(str(params["dcm_sense2world"]["row_1"][1]))
        self.lineEdit_dcm02.setText(str(params["dcm_sense2world"]["row_1"][2]))
        self.lineEdit_dcm10.setText(str(params["dcm_sense2world"]["row_2"][0]))
        self.lineEdit_dcm11.setText(str(params["dcm_sense2world"]["row_2"][1]))
        self.lineEdit_dcm12.setText(str(params["dcm_sense2world"]["row_2"][2]))
        self.lineEdit_dcm20.setText(str(params["dcm_sense2world"]["row_3"][0]))
        self.lineEdit_dcm21.setText(str(params["dcm_sense2world"]["row_3"][1]))
        self.lineEdit_dcm22.setText(str(params["dcm_sense2world"]["row_3"][2]))

        self.lineEdit_minx.setText(str(params["min_bounds"][0]))
        self.lineEdit_miny.setText(str(params["min_bounds"][1]))
        self.lineEdit_minz.setText(str(params["min_bounds"][2]))

        self.lineEdit_maxx.setText(str(params["max_bounds"][0]))
        self.lineEdit_maxy.setText(str(params["max_bounds"][1]))
        self.lineEdit_maxz.setText(str(params["max_bounds"][2]))

        self.lineEdit_conf.setText(str(params["conf_threshold"]))
        self.lineEdit_tex_conf.setText(str(params["tex_conf_threshold"]))

        self.checkBox_req_cal.setCheckState(bool(params["req_calibration"]))


# class DataManager(QObject):

#     loop_end = pyqtSignal(dict)

#     def __init__(self):
#         super().__init__()
#         self.rate = None
#         self.timer = None

#     @pyqtSlot()
#     def loop(self):


#         self.signal.emit(self.vehicles_list)
#         self.timer.start(self.rate)

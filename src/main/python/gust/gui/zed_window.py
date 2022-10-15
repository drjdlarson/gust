"""Logic for zed manager/viewer window."""
import requests
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer, QObject
from ruamel.yaml import YAML

from zed import ConfigSet
from gust.gui.ui.zed_window import Ui_ZedWindow
from gust.wsgi_apps.api.url_bases import BASE, ZED

URL_BASE = "http://localhost:8000/{}/{}/".format(BASE, ZED)
yaml = YAML()


class ZedWindow(QMainWindow, Ui_ZedWindow):
    """Main interface for the sensors selection window"""

    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)
        self.config = ConfigSet()
        # self.manager = DataManager()

        self.setupUi(self)

        self.action_Open_configuration.triggered.connect(self.load_config)

        self.pushButton_connect.clicked.connect(self.connect_clicked)
        self.pushButton_reset.clicked.connect(self.reset_clicked)

        self.lineEdit_id.textChanged.connect(self.id_changed)
        self.lineEdit_name.textChanged.connect(self.name_changed)

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

        self.reset_config_line_edits()

    def connect_clicked(self):
        url = "{}connect?".format(URL_BASE)
        url += "id={}&name={}".format(
            self.config.id, self.config.name.replace(" ", "_")
        )
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

    def reset_clicked(self):
        self.config = ConfigSet()
        self.reset_config_line_edits()

    def id_changed(self, e):
        try:
            new_id = int(self.lineEdit_id.text())
        except ValueError:
            return
        self.config.id = new_id

    def name_changed(self, e):
        self.config.name = self.lineEdit_name.text()

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

"""Logic for starting Ardupilot SIL"""
import requests
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtCore import pyqtSignal
from wsgi_apps.api.url_bases import BASE, DRONE
from gust.gui.ui.start_sil import Ui_Dialog

URL_BASE = "http://localhost:8000/{}/".format(BASE)
DRONE_BASE = "{}{}/".format(URL_BASE, DRONE)

# Add to this list to add more available Ardupilot Vehicle Types
VEHICLES = ["ArduCopter", "ArduPlane"]

class StartSILWindow(QDialog, Ui_Dialog):

    # signal to notify FrontEnd once a SIL is successfully started
    signal = pyqtSignal(str)

    def __init__(self, ctx, saved_locations):
        super().__init__()

        self.ctx = ctx
        self.saved_locations = saved_locations
        self.vehicle_type = None
        self.custom_home = False
        self.setupUi(self)

        self.comboBox_type.addItems(VEHICLES)
        self.comboBox_type.setCurrentIndex(0)
        self.vehicle_type = self.comboBox_type.currentText()

        # adding saved locations information
        self.comboBox_select_home.addItems(self.saved_locations.keys())
        self.comboBox_select_home.addItem("Custom")
        self.change_custom_home_visibility(False)
        self.comboBox_select_home.setCurrentIndex(0)

        # event connections
        self.comboBox_type.currentTextChanged.connect(self.vehicle_type_changed)
        self.comboBox_select_home.currentTextChanged.connect(self.home_location_changed)
        self.pushButton_start.clicked.connect(self.clicked_start)
        self.pushButton_cancel.clicked.connect(self.clicked_cancel)

    def home_location_changed(self):
        """Event connection for when new home location is selected"""
        if self.comboBox_select_home.currentText() == "Custom":
            self.custom_home = True
            self.change_custom_home_visibility(True)
        else:
            self.custom_home = False
            self.change_custom_home_visibility(False)

    def vehicle_type_changed(self):
        """Event connection when new vehicle type is selected"""
        self.vehicle_type = self.comboBox_type.currentText()

    def clicked_start(self):
        """Takes current selections and sends a request to start an Ardupilot SIL"""

        # initial URL
        url = "{}start_sil".format(DRONE_BASE)

        # SIL vehicle name
        sil_name = self.lineEdit_sil_name.text()
        if sil_name is not None:
            url += "?sil_name={}".format(sil_name)
        else:
            self.show_message_box("SIL name not specified")
            return

        # SIL vehicle type
        url += "&vehicle_type={}".format(self.vehicle_type.lower())

        # getting location information for where to start the SIL vehicle
        if self.custom_home:
            home_string = self.set_home_location_string(
                self.lineEdit_home_lat.text(),
                self.lineEdit_home_lon.text(),
                self.lineEdit_start_altitude.text(),
                self.lineEdit_start_heading.text(),
            )
        else:
            # loading pre saved position info from saved_locations.
            self.home_location = self.comboBox_select_home.currentText()
            home_string = self.set_home_location_string(
                self.saved_locations[self.home_location][0],
                self.saved_locations[self.home_location][1],
                self.lineEdit_start_altitude.text(),
                self.lineEdit_start_heading.text(),
            )
        url += "&home={}".format(home_string)

        # final URL
        start_sil = requests.get(url).json()


        if start_sil["success"]:
            # this signal is received by FrontendWindow after SIL is started successfully
            self.signal.emit(sil_name)
            self.show_message_box(QMessageBox.Information, "Started SIL")
            self.accept()

        else:
            self.show_message_box(
                QMessageBox.Warning,
                "Failed starting SIL: <<{:s}>>".format(start_sil["msg"]),
            )

    def show_message_box(self, qmsg_type, msg):
        """
        Display message to the user

        Parameters
        ----------
        qmsg_type: QMessageBox::Icon
            Icon type (example: QMessageBox.Warning)
        msg: str
            String message for display to the user

        Returns
        -------

        """
        msgBox = QMessageBox()
        msgBox.setIcon(qmsg_type)
        msgBox.setText(msg)
        msgBox.exec()

    def clicked_cancel(self):
        """Closes the window"""
        self.reject()

    def change_custom_home_visibility(self, val):
        """
        Change the boxes visibility for home lat and lon
        Parameters
        ----------
        val: bool
            Hide or display the boxes

        Returns
        -------

        """
        self.lineEdit_home_lon.setEnabled(val)
        self.lineEdit_home_lat.setEnabled(val)

    def set_home_location_string(self, lat, lon, alt, hdg):
        """Formats the home position into a string"""
        return "{},{},{},{}".format(lat, lon, alt, hdg)

    def setupUi(self, mainWindow):
        """Sets up user interface"""
        super().setupUi(mainWindow)
        self.home_location = 'SHELBY'
        self.lineEdit_start_altitude.setText("100")
        self.lineEdit_start_heading.setText("45")

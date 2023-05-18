"""Logic for RC Channels display window"""
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from gust.gui.ui.generic_channels import Ui_MainWindow

class RCWindow(QMainWindow, Ui_MainWindow):
    """Main interface for the RC channels window"""

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setupUi(self)

        self.chancount = 16
        self.rssi = 80

        self.label_heading.setText("RC Channels")

        self.label_rssi = QtWidgets.QLabel(self.verticalWidget_common)
        self.label_rssi.setAlignment(QtCore.Qt.AlignCenter)
        self.label_rssi.setObjectName("label_rssi")
        self.label_rssi.setText("rssi: {}".format(self.rssi))
        self.label_rssi.setAlignment(QtCore.Qt.AlignLeft)
        self.verticalLayout.addWidget(self.label_rssi)

        self.label_chancount = QtWidgets.QLabel(self.verticalWidget_common)
        self.label_chancount.setAlignment(QtCore.Qt.AlignCenter)
        self.label_chancount.setObjectName("label_chancount")
        self.label_chancount.setText("Channels Count: {}".format(self.chancount))
        self.label_chancount.setAlignment(QtCore.Qt.AlignLeft)
        self.verticalLayout.addWidget(self.label_chancount)

        self.label_chan = {}
        self.progressBar = {}

        # Manually creating all the UI elements for RC channel label and bar
        for i in range(self.chancount):
            chan = i + 1

            self.verticalWidget_each = QtWidgets.QWidget(self.centralwidget)
            self.verticalWidget_each.setMinimumSize(QtCore.QSize(210, 70))
            self.verticalWidget_each.setMaximumSize(QtCore.QSize(16777215, 100))
            self.verticalWidget_each.setObjectName("verticalWidget_each")
            self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalWidget_each)
            self.verticalLayout_2.setContentsMargins(10, 20, 10, 10)
            self.verticalLayout_2.setObjectName("verticalLayout_2")

            self.label_chan[chan] = QtWidgets.QLabel(self.verticalWidget_each)
            self.label_chan_name = self.label_chan[chan]
            self.label_chan_name.setMaximumSize(QtCore.QSize(16777215, 20))
            self.label_chan_name.setObjectName("label_chan_name")
            self.label_chan_name.setText("RC Channel {}".format(chan))
            self.verticalLayout_2.addWidget(self.label_chan_name)

            self.progressBar[chan] = QtWidgets.QProgressBar(self.verticalWidget_each)
            self.progressBar_pwm = self.progressBar[chan]
            self.progressBar_pwm.setStyleSheet("")
            self.progressBar_pwm.setMinimum(800)
            self.progressBar_pwm.setMaximum(2200)
            self.progressBar_pwm.setProperty("value", 1000)
            self.progressBar_pwm.setOrientation(QtCore.Qt.Horizontal)
            self.progressBar_pwm.setObjectName("progressBar_pwm")
            self.progressBar_pwm.setFormat("%v")
            self.verticalLayout_2.addWidget(self.progressBar_pwm)

            if chan % 2 == 0:
                column = 1
                row = chan - 1
            else:
                column = 0
                row = chan
            self.gridLayout_chan.addWidget(self.verticalWidget_each, row, column)

    def set_RCvalue(self, chan, value):
        """
        Set Values to the RC channels

        Parameters
        ----------
        chan: int
            Channel Number
        value: int
            RC Channel PWN value

        Returns
        -------

        """
        self.progressBar[chan].setProperty("value", value)

    def setupUi(self, mainWindow):
        """Sets up the user interface"""
        super().setupUi(mainWindow)

if __name__ == '__main__':
    app =QApplication(sys.argv)
    myApp = RCWindow()
    myApp.show()

    myApp.set_RCvalue(3, 2000)

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

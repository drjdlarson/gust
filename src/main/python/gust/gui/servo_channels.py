#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 10:26:29 2022

@author: lagerprocessor
"""

import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout

from gust.gui.ui.generic_channels import Ui_MainWindow

class ServoChannels(QMainWindow, Ui_MainWindow):
    """Main interface for the servo channels window"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.servo_port = 0
        self.servo_count = 16

        self.label_heading.setText("Servo Channels")

        self.label_port = QtWidgets.QLabel(self.verticalWidget_common)
        self.label_port.setAlignment(QtCore.Qt.AlignCenter)
        self.label_port.setObjectName("label_port")
        self.label_port.setText("port: {}".format(self.servo_port))
        self.label_port.setAlignment(QtCore.Qt.AlignLeft)
        self.verticalLayout.addWidget(self.label_port)

        self.label_chan = {}
        self.progressBar = {}

        for i in range(self.servo_count):
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
            self.label_chan_name.setText("Servo Channel {}".format(chan))
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

    def set_servo_value(self, chan, value):
        self.progressBar[chan].setProperty("value", value)

if __name__ == '__main__':
    app =QApplication(sys.argv)
    myApp = ServoChannels()
    myApp.show()

    myApp.set_servo_value(3, 2000)

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:19:09 2022

@author: lagerprocessor
"""

import sys
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFrame
from PyQt5.QtGui import QIcon, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt

class HudWidget(QWidget):
    def __init__(self,*args,**kwargs):
        QWidget.__init__(self,*args,**kwargs)
        self.setWindowTitle('Heads up Display GUST')
        self.setMinimumSize(QtCore.QSize(308,308))
        self.setStyleSheet("background-color:rgb(172,212,255)")
        self.setMouseTracking(False)
        width=self.frameGeometry().width()
        height=self.frameGeometry().height()
        centerx=width/2
        centery=height/2

        def draw_




#Main layout of the widget
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)


# top layout of the widget (includes Bearing)
        self.horizontallayout_top=QtWidgets.QHBoxLayout()
        self.horizontallayout_top.setObjectName("horizontallayout_top")
        self.frame_top=QtWidgets.QFrame()
        sizePolicy=QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_top.sizePolicy().hasHeightForWidth())
        self.frame_top.setSizePolicy(sizePolicy)
        self.frame_top.setMinimumSize(QtCore.QSize(308,25))
        self.frame_top.setMaximumSize(QtCore.QSize(180,16777215))
        self.frame_top.setAutoFillBackground(False)
        self.frame_top.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top.setObjectName("frame_top")

        self.horizontallayout_top.addWidget(self.frame_top)

        main_layout.addLayout(self.horizontallayout_top)

#Mid Layout of the widget (includes Airspeed frame, horizon frame, and altitude frame)
        self.horizontallayout_mid=QtWidgets.QHBoxLayout()
        self.horizontallayout_mid.setObjectName("horizontallayout_mid")

        #airspeed frame
        self.frame_airspeed=QtWidgets.QFrame()
        sizePolicy=QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_airspeed.sizePolicy().hasHeightForWidth())
        self.frame_airspeed.setSizePolicy(sizePolicy)
        self.frame_airspeed.setMinimumSize(QtCore.QSize(30,150))
        self.frame_airspeed.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_airspeed.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_airspeed.setObjectName("frame_airspeed")
        self.horizontallayout_mid.addWidget(self.frame_airspeed)

        #horizon frame_
        self.frame_horizon=QtWidgets.QFrame()
        self.frame_horizon.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_horizon.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_horizon.setObjectName("frame_horizon")
        self.horizontallayout_mid.addWidget(self.frame_horizon)

        #altitude frame
        self.frame_altitude=QtWidgets.QFrame()
        sizePolicy=QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_altitude.sizePolicy().hasHeightForWidth())
        self.frame_altitude.setSizePolicy(sizePolicy)
        self.frame_altitude.setMinimumSize(QtCore.QSize(30,150))
        self.frame_altitude.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_altitude.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_altitude.setObjectName("frame_altitude")
        self.horizontallayout_mid.addWidget(self.frame_altitude)

        self.horizontallayout_mid.setStretch(1,1)

        main_layout.addLayout(self.horizontallayout_mid)

#Bottom layout of the widget (includes Status display)
        self.horizontallayout_bottom=QtWidgets.QHBoxLayout()
        self.horizontallayout_bottom.setObjectName("horizontallayout_bottom")

        #GPS Status label
        self.label_gnss=QtWidgets.QLabel()
        font=QtGui.QFont()
        font.setFamily("Padauk Book [PYRS]")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_gnss.setFont(font)
        self.label_gnss.setText("NO FIX")
        #self.label_gnss.setText("3D FIX")
        self.label_gnss.setStyleSheet("color:rgb(255,0,0)")
        self.label_gnss.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_gnss.setAlignment(QtCore.Qt.AlignCenter)
        self.label_gnss.setObjectName("label_gnss")

        self.horizontallayout_bottom.addWidget(self.label_gnss)

        #arming status label
        self.label_arm=QtWidgets.QLabel()
        self.label_arm.setFont(font)
        self.label_arm.setText("DISARMED")
        #self.label_arm.setText("ARMED")
        self.label_arm.setStyleSheet("color:rgb(255,0,0)")
        self.label_arm.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_arm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_arm.setObjectName("label_arm")
        self.horizontallayout_bottom.addWidget(self.label_arm)

        #GPS Status mode
        self.label_mode=QtWidgets.QLabel()
        self.label_mode.setFont(font)
        self.label_mode.setText("STABILIZE")
        #self.label_mode.setText("AUTO")
        self.label_mode.setStyleSheet("color:rgb(255,0,0)")
        self.label_mode.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_mode.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mode.setObjectName("label_mode")
        self.horizontallayout_bottom.addWidget(self.label_mode)

        main_layout.addLayout(self.horizontallayout_bottom)
        main_layout.setStretch(1, 1)



    # def paintEvent(self,event):
    #     painter=QPainter(self)
    #     painter.setPen(QPen(Qt.black,6))

    #     painter.drawLine(100,100,300,100)









if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = HudWidget()
    myApp.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

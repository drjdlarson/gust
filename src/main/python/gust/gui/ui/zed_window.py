# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/workspaces/gust/src/main/python/gust/gui/ui/zed_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ZedWindow(object):
    def setupUi(self, ZedWindow):
        ZedWindow.setObjectName("ZedWindow")
        ZedWindow.resize(1254, 690)
        self.centralwidget = QtWidgets.QWidget(ZedWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_dcm01 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_dcm01.setObjectName("lineEdit_dcm01")
        self.gridLayout_2.addWidget(self.lineEdit_dcm01, 0, 1, 1, 1)
        self.lineEdit_dcm00 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_dcm00.setObjectName("lineEdit_dcm00")
        self.gridLayout_2.addWidget(self.lineEdit_dcm00, 0, 0, 1, 1)
        self.lineEdit_dcm02 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_dcm02.setObjectName("lineEdit_dcm02")
        self.gridLayout_2.addWidget(self.lineEdit_dcm02, 0, 2, 1, 1)
        self.lineEdit_dcm10 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_dcm10.setObjectName("lineEdit_dcm10")
        self.gridLayout_2.addWidget(self.lineEdit_dcm10, 1, 0, 1, 1)
        self.lineEdit_dcm20 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_dcm20.setObjectName("lineEdit_dcm20")
        self.gridLayout_2.addWidget(self.lineEdit_dcm20, 2, 0, 1, 1)
        self.lineEdit_dcm11 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_dcm11.setObjectName("lineEdit_dcm11")
        self.gridLayout_2.addWidget(self.lineEdit_dcm11, 1, 1, 1, 1)
        self.lineEdit_dcm12 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_dcm12.setObjectName("lineEdit_dcm12")
        self.gridLayout_2.addWidget(self.lineEdit_dcm12, 1, 2, 1, 1)
        self.lineEdit_dcm21 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_dcm21.setObjectName("lineEdit_dcm21")
        self.gridLayout_2.addWidget(self.lineEdit_dcm21, 2, 1, 1, 1)
        self.lineEdit_dcm22 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_dcm22.setObjectName("lineEdit_dcm22")
        self.gridLayout_2.addWidget(self.lineEdit_dcm22, 2, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 4, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 5, 0, 1, 1)
        self.label_name = QtWidgets.QLabel(self.centralwidget)
        self.label_name.setObjectName("label_name")
        self.gridLayout_3.addWidget(self.label_name, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 7, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 8, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lineEdit_id = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.horizontalLayout_5.addWidget(self.lineEdit_id)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 4, 0, 1, 1)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.lineEdit_tex_conf = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_tex_conf.setObjectName("lineEdit_tex_conf")
        self.horizontalLayout_15.addWidget(self.lineEdit_tex_conf)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem1)
        self.gridLayout_3.addLayout(self.horizontalLayout_15, 9, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 6, 0, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_12.addWidget(self.label_20)
        self.lineEdit_minx = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_minx.setObjectName("lineEdit_minx")
        self.horizontalLayout_12.addWidget(self.lineEdit_minx)
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_12.addWidget(self.label_19)
        self.lineEdit_miny = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_miny.setObjectName("lineEdit_miny")
        self.horizontalLayout_12.addWidget(self.lineEdit_miny)
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_12.addWidget(self.label_18)
        self.lineEdit_minz = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_minz.setObjectName("lineEdit_minz")
        self.horizontalLayout_12.addWidget(self.lineEdit_minz)
        self.gridLayout_3.addLayout(self.horizontalLayout_12, 6, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 9, 0, 1, 1)
        self.label_loc = QtWidgets.QLabel(self.centralwidget)
        self.label_loc.setObjectName("label_loc")
        self.gridLayout_3.addWidget(self.label_loc, 3, 0, 1, 1)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.lineEdit_conf = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_conf.setObjectName("lineEdit_conf")
        self.horizontalLayout_14.addWidget(self.lineEdit_conf)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem2)
        self.gridLayout_3.addLayout(self.horizontalLayout_14, 8, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_locx = QtWidgets.QLabel(self.centralwidget)
        self.label_locx.setObjectName("label_locx")
        self.horizontalLayout_4.addWidget(self.label_locx)
        self.lineEdit_locx = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_locx.setObjectName("lineEdit_locx")
        self.horizontalLayout_4.addWidget(self.lineEdit_locx)
        self.label_locy = QtWidgets.QLabel(self.centralwidget)
        self.label_locy.setObjectName("label_locy")
        self.horizontalLayout_4.addWidget(self.label_locy)
        self.lineEdit_locy = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_locy.setObjectName("lineEdit_locy")
        self.horizontalLayout_4.addWidget(self.lineEdit_locy)
        self.label_locz = QtWidgets.QLabel(self.centralwidget)
        self.label_locz.setObjectName("label_locz")
        self.horizontalLayout_4.addWidget(self.label_locz)
        self.lineEdit_locz = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_locz.setObjectName("lineEdit_locz")
        self.horizontalLayout_4.addWidget(self.lineEdit_locz)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 3, 1, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_13.addWidget(self.label_22)
        self.lineEdit_maxx = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_maxx.setObjectName("lineEdit_maxx")
        self.horizontalLayout_13.addWidget(self.lineEdit_maxx)
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_13.addWidget(self.label_23)
        self.lineEdit_maxy = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_maxy.setObjectName("lineEdit_maxy")
        self.horizontalLayout_13.addWidget(self.lineEdit_maxy)
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_13.addWidget(self.label_21)
        self.lineEdit_maxz = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_maxz.setObjectName("lineEdit_maxz")
        self.horizontalLayout_13.addWidget(self.lineEdit_maxz)
        self.gridLayout_3.addLayout(self.horizontalLayout_13, 7, 1, 1, 1)
        self.label_id = QtWidgets.QLabel(self.centralwidget)
        self.label_id.setObjectName("label_id")
        self.gridLayout_3.addWidget(self.label_id, 0, 0, 1, 1)
        self.checkBox_req_cal = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_req_cal.setText("")
        self.checkBox_req_cal.setObjectName("checkBox_req_cal")
        self.gridLayout_3.addWidget(self.checkBox_req_cal, 5, 1, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lineEdit_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.horizontalLayout_6.addWidget(self.lineEdit_name)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 1, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setObjectName("label_25")
        self.gridLayout_3.addWidget(self.label_25, 2, 0, 1, 1)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.lineEdit_update_rate = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_update_rate.setObjectName("lineEdit_update_rate")
        self.horizontalLayout_16.addWidget(self.lineEdit_update_rate)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem4)
        self.gridLayout_3.addLayout(self.horizontalLayout_16, 2, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_7.addWidget(self.label_8)
        self.lineEdit_cal_minx = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cal_minx.setObjectName("lineEdit_cal_minx")
        self.horizontalLayout_7.addWidget(self.lineEdit_cal_minx)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_7.addWidget(self.label_9)
        self.lineEdit_cal_miny = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cal_miny.setObjectName("lineEdit_cal_miny")
        self.horizontalLayout_7.addWidget(self.lineEdit_cal_miny)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_7.addWidget(self.label_10)
        self.lineEdit_cal_minz = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cal_minz.setObjectName("lineEdit_cal_minz")
        self.horizontalLayout_7.addWidget(self.lineEdit_cal_minz)
        self.gridLayout_5.addLayout(self.horizontalLayout_7, 0, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem5, 0, 2, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.groupBox)
        self.label_16.setObjectName("label_16")
        self.gridLayout_5.addWidget(self.label_16, 3, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_8.addWidget(self.label_12)
        self.lineEdit_cal_maxx = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cal_maxx.setObjectName("lineEdit_cal_maxx")
        self.horizontalLayout_8.addWidget(self.lineEdit_cal_maxx)
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_8.addWidget(self.label_14)
        self.lineEdit_cal_maxy = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cal_maxy.setObjectName("lineEdit_cal_maxy")
        self.horizontalLayout_8.addWidget(self.lineEdit_cal_maxy)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_8.addWidget(self.label_13)
        self.lineEdit_cal_maxz = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cal_maxz.setObjectName("lineEdit_cal_maxz")
        self.horizontalLayout_8.addWidget(self.lineEdit_cal_maxz)
        self.gridLayout_5.addLayout(self.horizontalLayout_8, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 1, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setObjectName("label_15")
        self.gridLayout_5.addWidget(self.label_15, 2, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.groupBox)
        self.label_17.setObjectName("label_17")
        self.gridLayout_5.addWidget(self.label_17, 4, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.lineEdit_cal_roll = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cal_roll.setObjectName("lineEdit_cal_roll")
        self.horizontalLayout_9.addWidget(self.lineEdit_cal_roll)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem6)
        self.gridLayout_5.addLayout(self.horizontalLayout_9, 2, 1, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.lineEdit_cal_pitch = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cal_pitch.setObjectName("lineEdit_cal_pitch")
        self.horizontalLayout_10.addWidget(self.lineEdit_cal_pitch)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem7)
        self.gridLayout_5.addLayout(self.horizontalLayout_10, 3, 1, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.lineEdit_cal_yaw = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cal_yaw.setObjectName("lineEdit_cal_yaw")
        self.horizontalLayout_11.addWidget(self.lineEdit_cal_yaw)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem8)
        self.gridLayout_5.addLayout(self.horizontalLayout_11, 4, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem9 = QtWidgets.QSpacerItem(20, 531, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem9)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem10)
        self.pushButton_reset = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.horizontalLayout_3.addWidget(self.pushButton_reset)
        self.pushButton_disconnect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_disconnect.setStyleSheet("background-color: red")
        self.pushButton_disconnect.setObjectName("pushButton_disconnect")
        self.horizontalLayout_3.addWidget(self.pushButton_disconnect)
        self.pushButton_connect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connect.setStyleSheet("background-color: green")
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.horizontalLayout_3.addWidget(self.pushButton_connect)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        self.label_24.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout.addWidget(self.label_24)
        self.lineEdit_plot_rate = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_plot_rate.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_plot_rate.setObjectName("lineEdit_plot_rate")
        self.horizontalLayout.addWidget(self.lineEdit_plot_rate)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem11)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget_graphs = GraphicsLayoutWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_graphs.sizePolicy().hasHeightForWidth())
        self.widget_graphs.setSizePolicy(sizePolicy)
        self.widget_graphs.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_graphs.setBaseSize(QtCore.QSize(0, 0))
        self.widget_graphs.setObjectName("widget_graphs")
        self.verticalLayout.addWidget(self.widget_graphs)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        ZedWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ZedWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1254, 22))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        ZedWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ZedWindow)
        self.statusbar.setObjectName("statusbar")
        ZedWindow.setStatusBar(self.statusbar)
        self.action_Open_configuration = QtWidgets.QAction(ZedWindow)
        self.action_Open_configuration.setObjectName("action_Open_configuration")
        self.menu_File.addAction(self.action_Open_configuration)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(ZedWindow)
        QtCore.QMetaObject.connectSlotsByName(ZedWindow)

    def retranslateUi(self, ZedWindow):
        _translate = QtCore.QCoreApplication.translate
        ZedWindow.setWindowTitle(_translate("ZedWindow", "ZED Manager"))
        self.label_2.setText(_translate("ZedWindow", "Require Calibration:"))
        self.label_name.setText(_translate("ZedWindow", "Name:"))
        self.label_4.setText(_translate("ZedWindow", "Max Bounds (cage):"))
        self.label_5.setText(_translate("ZedWindow", "Confidence:"))
        self.label.setText(_translate("ZedWindow", "DCM Sensor to World:"))
        self.label_3.setText(_translate("ZedWindow", "Min Bounds (cage):"))
        self.label_20.setText(_translate("ZedWindow", "x:"))
        self.label_19.setText(_translate("ZedWindow", "y:"))
        self.label_18.setText(_translate("ZedWindow", "z:"))
        self.label_6.setText(_translate("ZedWindow", "Texture Confidence:"))
        self.label_loc.setText(_translate("ZedWindow", "Location in World:"))
        self.label_locx.setText(_translate("ZedWindow", "x:"))
        self.label_locy.setText(_translate("ZedWindow", "y:"))
        self.label_locz.setText(_translate("ZedWindow", "z:"))
        self.label_22.setText(_translate("ZedWindow", "x:"))
        self.label_23.setText(_translate("ZedWindow", "y:"))
        self.label_21.setText(_translate("ZedWindow", "z:"))
        self.label_id.setText(_translate("ZedWindow", "ID:"))
        self.label_25.setText(_translate("ZedWindow", "Update Rate (Hz):"))
        self.groupBox.setTitle(_translate("ZedWindow", "Calibration Parameters"))
        self.label_8.setText(_translate("ZedWindow", "x:"))
        self.label_9.setText(_translate("ZedWindow", "y:"))
        self.label_10.setText(_translate("ZedWindow", "z:"))
        self.label_16.setText(_translate("ZedWindow", "Pitch sensor to world (deg):"))
        self.label_12.setText(_translate("ZedWindow", "x:"))
        self.label_14.setText(_translate("ZedWindow", "y:"))
        self.label_13.setText(_translate("ZedWindow", "z:"))
        self.label_7.setText(_translate("ZedWindow", "Min Bounds (sensor):"))
        self.label_11.setText(_translate("ZedWindow", "Max Bounds (sensor):"))
        self.label_15.setText(_translate("ZedWindow", "Roll sensor to world (deg):"))
        self.label_17.setText(_translate("ZedWindow", "Yaw sensor to world (deg):"))
        self.pushButton_reset.setText(_translate("ZedWindow", "&Reset"))
        self.pushButton_disconnect.setText(_translate("ZedWindow", "Disconnect"))
        self.pushButton_connect.setText(_translate("ZedWindow", "&Connect"))
        self.label_24.setText(_translate("ZedWindow", "Plotting Rate (Hz):"))
        self.menu_File.setTitle(_translate("ZedWindow", "&File"))
        self.action_Open_configuration.setText(_translate("ZedWindow", "&Open configuration"))
from pyqtgraph import GraphicsLayoutWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ZedWindow = QtWidgets.QMainWindow()
    ui = Ui_ZedWindow()
    ui.setupUi(ZedWindow)
    ZedWindow.show()
    sys.exit(app.exec_())

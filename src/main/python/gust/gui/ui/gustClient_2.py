# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/gust/gui/ui/gustClient_2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
import io
import folium

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1301, 909)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(211, 215, 207);")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.widget_main = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_main.sizePolicy().hasHeightForWidth())
        self.widget_main.setSizePolicy(sizePolicy)
        self.widget_main.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget_main.setAutoFillBackground(False)
        self.widget_main.setObjectName("widget_main")
        self.verticalWidget = QtWidgets.QWidget(self.widget_main)
        self.verticalWidget.setGeometry(QtCore.QRect(9, 9, 326, 528))
        self.verticalWidget.setMaximumSize(QtCore.QSize(450, 16777215))
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView_dummyHUD = QtWidgets.QGraphicsView(self.verticalWidget)
        self.graphicsView_dummyHUD.setMaximumSize(QtCore.QSize(500, 500))
        self.graphicsView_dummyHUD.setObjectName("graphicsView_dummyHUD")
        self.verticalLayout.addWidget(self.graphicsView_dummyHUD)
        self.label_seluav = QtWidgets.QLabel(self.verticalWidget)
        self.label_seluav.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_seluav.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"color: rgb(0, 0, 0);\n"
"font: 75 20pt \"URW Bookman L\";")
        self.label_seluav.setAlignment(QtCore.Qt.AlignCenter)
        self.label_seluav.setObjectName("label_seluav")
        self.verticalLayout.addWidget(self.label_seluav)
        self.formLayout_3 = QtWidgets.QWidget(self.verticalWidget)
        self.formLayout_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.formLayout_3.setStyleSheet("background-color: rgb(195, 204, 147);")
        self.formLayout_3.setObjectName("formLayout_3")
        self.formLayout_info = QtWidgets.QFormLayout(self.formLayout_3)
        self.formLayout_info.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout_info.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_info.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        self.formLayout_info.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_info.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_info.setContentsMargins(5, 5, 5, 5)
        self.formLayout_info.setHorizontalSpacing(40)
        self.formLayout_info.setVerticalSpacing(5)
        self.formLayout_info.setObjectName("formLayout_info")
        self.lcdNumber_altitude = QtWidgets.QLCDNumber(self.formLayout_3)
        self.lcdNumber_altitude.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lcdNumber_altitude.setFont(font)
        self.lcdNumber_altitude.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_altitude.setStyleSheet("color: rgb(243, 243, 243);\n"
"font: 75 11pt \"Ubuntu Condensed\";\n"
"background-color: rgb(85, 87, 83);")
        self.lcdNumber_altitude.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber_altitude.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_altitude.setObjectName("lcdNumber_altitude")
        self.formLayout_info.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lcdNumber_altitude)
        self.lcdNumber_vspeed = QtWidgets.QLCDNumber(self.formLayout_3)
        self.lcdNumber_vspeed.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lcdNumber_vspeed.setFont(font)
        self.lcdNumber_vspeed.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_vspeed.setStyleSheet("color: rgb(243, 243, 243);\n"
"font: 75 11pt \"Ubuntu Condensed\";\n"
"background-color: rgb(85, 87, 83);")
        self.lcdNumber_vspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber_vspeed.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_vspeed.setObjectName("lcdNumber_vspeed")
        self.formLayout_info.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lcdNumber_vspeed)
        self.label_altitude = QtWidgets.QLabel(self.formLayout_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_altitude.sizePolicy().hasHeightForWidth())
        self.label_altitude.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_altitude.setFont(font)
        self.label_altitude.setStatusTip("")
        self.label_altitude.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"font: 75 15pt \"Waree\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.label_altitude.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_altitude.setAlignment(QtCore.Qt.AlignCenter)
        self.label_altitude.setObjectName("label_altitude")
        self.formLayout_info.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_altitude)
        self.label_vspeed = QtWidgets.QLabel(self.formLayout_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_vspeed.sizePolicy().hasHeightForWidth())
        self.label_vspeed.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_vspeed.setFont(font)
        self.label_vspeed.setStatusTip("")
        self.label_vspeed.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"font: 75 15pt \"Waree\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.label_vspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_vspeed.setAlignment(QtCore.Qt.AlignCenter)
        self.label_vspeed.setObjectName("label_vspeed")
        self.formLayout_info.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.label_vspeed)
        self.lcdNumber_airspeed = QtWidgets.QLCDNumber(self.formLayout_3)
        self.lcdNumber_airspeed.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lcdNumber_airspeed.setFont(font)
        self.lcdNumber_airspeed.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_airspeed.setStyleSheet("color: rgb(243, 243, 243);\n"
"font: 75 11pt \"Ubuntu Condensed\";\n"
"background-color: rgb(85, 87, 83);")
        self.lcdNumber_airspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber_airspeed.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_airspeed.setObjectName("lcdNumber_airspeed")
        self.formLayout_info.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.lcdNumber_airspeed)
        self.lcdNumber_gndspeed = QtWidgets.QLCDNumber(self.formLayout_3)
        self.lcdNumber_gndspeed.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lcdNumber_gndspeed.setFont(font)
        self.lcdNumber_gndspeed.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_gndspeed.setStyleSheet("color: rgb(243, 243, 243);\n"
"font: 75 11pt \"Ubuntu Condensed\";\n"
"background-color: rgb(85, 87, 83);")
        self.lcdNumber_gndspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber_gndspeed.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_gndspeed.setObjectName("lcdNumber_gndspeed")
        self.formLayout_info.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lcdNumber_gndspeed)
        self.label_airspeed = QtWidgets.QLabel(self.formLayout_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_airspeed.sizePolicy().hasHeightForWidth())
        self.label_airspeed.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_airspeed.setFont(font)
        self.label_airspeed.setStatusTip("")
        self.label_airspeed.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"font: 75 15pt \"Waree\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.label_airspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_airspeed.setAlignment(QtCore.Qt.AlignCenter)
        self.label_airspeed.setObjectName("label_airspeed")
        self.formLayout_info.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_airspeed)
        self.label_gndspeed = QtWidgets.QLabel(self.formLayout_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_gndspeed.sizePolicy().hasHeightForWidth())
        self.label_gndspeed.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_gndspeed.setFont(font)
        self.label_gndspeed.setStatusTip("")
        self.label_gndspeed.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"font: 75 15pt \"Waree\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.label_gndspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_gndspeed.setAlignment(QtCore.Qt.AlignCenter)
        self.label_gndspeed.setObjectName("label_gndspeed")
        self.formLayout_info.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.label_gndspeed)
        self.lcdNumber_voltage = QtWidgets.QLCDNumber(self.formLayout_3)
        self.lcdNumber_voltage.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lcdNumber_voltage.setFont(font)
        self.lcdNumber_voltage.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_voltage.setStyleSheet("color: rgb(243, 243, 243);\n"
"font: 75 11pt \"Ubuntu Condensed\";\n"
"background-color: rgb(85, 87, 83);")
        self.lcdNumber_voltage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber_voltage.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_voltage.setObjectName("lcdNumber_voltage")
        self.formLayout_info.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.lcdNumber_voltage)
        self.lcdNumber_current = QtWidgets.QLCDNumber(self.formLayout_3)
        self.lcdNumber_current.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lcdNumber_current.setFont(font)
        self.lcdNumber_current.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_current.setStyleSheet("color: rgb(243, 243, 243);\n"
"font: 75 11pt \"Ubuntu Condensed\";\n"
"background-color: rgb(85, 87, 83);")
        self.lcdNumber_current.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber_current.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_current.setObjectName("lcdNumber_current")
        self.formLayout_info.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.lcdNumber_current)
        self.label_voltage = QtWidgets.QLabel(self.formLayout_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_voltage.sizePolicy().hasHeightForWidth())
        self.label_voltage.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_voltage.setFont(font)
        self.label_voltage.setStatusTip("")
        self.label_voltage.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"font: 75 15pt \"Waree\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.label_voltage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_voltage.setAlignment(QtCore.Qt.AlignCenter)
        self.label_voltage.setObjectName("label_voltage")
        self.formLayout_info.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_voltage)
        self.label_current = QtWidgets.QLabel(self.formLayout_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_current.sizePolicy().hasHeightForWidth())
        self.label_current.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_current.setFont(font)
        self.label_current.setStatusTip("")
        self.label_current.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"font: 75 15pt \"Waree\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.label_current.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_current.setAlignment(QtCore.Qt.AlignCenter)
        self.label_current.setObjectName("label_current")
        self.formLayout_info.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.label_current)
        self.verticalLayout.addWidget(self.formLayout_3)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.widget_main)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(465, 75, 721, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_addrow = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_addrow.setObjectName("pushButton_addrow")
        self.horizontalLayout.addWidget(self.pushButton_addrow)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 200))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.verticalLayout_2.addWidget(self.tableWidget)

        coordinate=(30,30)
        m=folium.Map(
            tiles='Stamen Terrain',
            zoom_start=13,
            location=coordinate
            )
        data=io.BytesIO()
        m.save(data,close_file=False)

        webView=QWebEngineView()
        webView.setHtml(data.getvalue().decode())


        self.quickWidget_maptest = QtQuickWidgets.QQuickWidget(self.widget_main)
        self.quickWidget_maptest.setGeometry(QtCore.QRect(570, 400, 300, 200))
        self.quickWidget_maptest.setResizeMode(QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        self.quickWidget_maptest.setObjectName("quickWidget_maptest")



        MainWindow.setCentralWidget(self.widget_main)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.widget_main.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_seluav.setText(_translate("MainWindow", "Current DRONE NAME"))
        self.label_altitude.setText(_translate("MainWindow", "Altitude"))
        self.label_vspeed.setText(_translate("MainWindow", "V. Speed"))
        self.label_airspeed.setText(_translate("MainWindow", "Airspeed"))
        self.label_gndspeed.setText(_translate("MainWindow", "Gnd. Speed"))
        self.label_voltage.setText(_translate("MainWindow", "Voltage"))
        self.label_current.setText(_translate("MainWindow", "Current"))
        self.pushButton_addrow.setText(_translate("MainWindow", "Add a vehicle"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "VEHICLE"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "MODE"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "FLYING TO"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "TIME IN AIR"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "ALTITUDE"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "VOLTAGE"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "CURRENT"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "DISCONNECT"))
from PyQt5 import QtQuickWidgets


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
